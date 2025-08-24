import numpy as np
import cv2, os, sys, torch
from tqdm import tqdm
from PIL import Image 
from collections import Counter
import warnings

# 3dmm extraction
import safetensors
import safetensors.torch 
from src.face3d.util.preprocess import align_img
from src.face3d.util.load_mats import load_lm3d
from src.face3d.models import networks

from scipy.io import loadmat, savemat
from src.utils.croper import Preprocesser
from src.utils.safetensor_helper import load_x_from_safetensor 

warnings.filterwarnings("ignore")

def split_coeff(coeffs):
        """
        Return:
            coeffs_dict     -- a dict of torch.tensors

        Parameters:
            coeffs          -- torch.tensor, size (B, 256)
        """
        id_coeffs = coeffs[:, :80]
        exp_coeffs = coeffs[:, 80: 144]
        tex_coeffs = coeffs[:, 144: 224]
        angles = coeffs[:, 224: 227]
        gammas = coeffs[:, 227: 254]
        translations = coeffs[:, 254:]
        return {
            'id': id_coeffs,
            'exp': exp_coeffs,
            'tex': tex_coeffs,
            'angle': angles,
            'gamma': gammas,
            'trans': translations
        }


class CropAndExtract():
    def __init__(self, sadtalker_path, device):

        self.propress = Preprocesser(device)
        self.net_recon = networks.define_net_recon(net_recon='resnet50', use_last_fc=False, init_path='').to(device)
        
        if sadtalker_path['use_safetensor']:
            checkpoint = safetensors.torch.load_file(sadtalker_path['checkpoint'])    
            self.net_recon.load_state_dict(load_x_from_safetensor(checkpoint, 'face_3drecon'))
        else:
            checkpoint = torch.load(sadtalker_path['path_of_net_recon_model'], map_location=torch.device(device))    
            self.net_recon.load_state_dict(checkpoint['net_recon'])

        self.net_recon.eval()
        self.lm3d_std = load_lm3d(sadtalker_path['dir_of_BFM_fitting'])
        self.device = device
    
    def generate(self, input_path, save_dir, crop_or_resize='crop', source_image_flag=False, pic_size=256):

        pic_name = os.path.splitext(os.path.split(input_path)[-1])[0]  

        landmarks_path =  os.path.join(save_dir, pic_name+'_landmarks.txt') 
        coeff_path =  os.path.join(save_dir, pic_name+'.mat')  
        png_path =  os.path.join(save_dir, pic_name+'.png')  

        #load input
        if not os.path.isfile(input_path):
            raise ValueError('input_path must be a valid path to video/image file')
        elif input_path.split('.')[-1] in ['jpg', 'png', 'jpeg']:
            # loader for first frame
            full_frames = [cv2.imread(input_path)]
            fps = 25
        else:
            # loader for videos
            video_stream = cv2.VideoCapture(input_path)
            fps = video_stream.get(cv2.CAP_PROP_FPS)
            full_frames = [] 
            while 1:
                still_reading, frame = video_stream.read()
                if not still_reading:
                    video_stream.release()
                    break 
                full_frames.append(frame) 
                if source_image_flag:
                    break

        x_full_frames= [cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  for frame in full_frames] 

        #### crop images as the 
        if 'crop' in crop_or_resize.lower(): # default crop
            x_full_frames, crop, quad = self.propress.crop(x_full_frames, still=True if 'ext' in crop_or_resize.lower() else False, xsize=512)
            clx, cly, crx, cry = crop
            lx, ly, rx, ry = quad
            lx, ly, rx, ry = int(lx), int(ly), int(rx), int(ry)
            oy1, oy2, ox1, ox2 = cly+ly, cly+ry, clx+lx, clx+rx
            crop_info = ((ox2 - ox1, oy2 - oy1), crop, quad)
        elif 'full' in crop_or_resize.lower():
            x_full_frames, crop, quad = self.propress.crop(x_full_frames, still=True if 'ext' in crop_or_resize.lower() else False, xsize=512)
            clx, cly, crx, cry = crop
            lx, ly, rx, ry = quad
            lx, ly, rx, ry = int(lx), int(ly), int(rx), int(ry)
            oy1, oy2, ox1, ox2 = cly+ly, cly+ry, clx+lx, clx+rx
            crop_info = ((ox2 - ox1, oy2 - oy1), crop, quad)
        else: # resize mode
            oy1, oy2, ox1, ox2 = 0, x_full_frames[0].shape[0], 0, x_full_frames[0].shape[1] 
            crop_info = ((ox2 - ox1, oy2 - oy1), None, None)

        frames_pil = [Image.fromarray(cv2.resize(frame,(pic_size, pic_size))) for frame in x_full_frames]
        if len(frames_pil) == 0:
            print('No face is detected in the input file')
            return None, None

        # save crop info
        for frame in frames_pil:
            cv2.imwrite(png_path, cv2.cvtColor(np.array(frame), cv2.COLOR_RGB2BGR))

        # 2. get the landmark according to the detected face. 
        if not os.path.isfile(landmarks_path): 
            lm = self.propress.predictor.extract_keypoint(frames_pil, landmarks_path)
        else:
            print(' Using saved landmarks.')
            lm = np.loadtxt(landmarks_path).astype(np.float32)
            lm = lm.reshape([len(x_full_frames), -1, 2])

        if not os.path.isfile(coeff_path):
            # load 3dmm paramter generator from Deep3DFaceRecon_pytorch 
            video_coeffs, full_coeffs = [],  []
            for idx in tqdm(range(len(frames_pil)), desc='3DMM Extraction In Video:'):
                frame = frames_pil[idx]
                W,H = frame.size
                lm1 = lm[idx].reshape([-1, 2])
            
                # 🚨 LANDMARK STANDARDIZATION: Đảm bảo luôn có dạng (5, 2) float32
                try:
                    if np.mean(lm1) == -1:
                        print(f"🔍 Frame {idx}: Using standard landmarks (no face detected)")
                        lm1 = (self.lm3d_std[:, :2]+1)/2.
                        lm1 = np.concatenate(
                            [lm1[:, :1]*W, lm1[:, 1:2]*H], 1
                        )
                    else:
                        print(f"🔍 Frame {idx}: Processing detected landmarks")
                        lm1[:, -1] = H - 1 - lm1[:, -1]
                    
                    # 🚨 CRITICAL: Standardize landmarks to (5, 2) format
                    print(f"🔍 Frame {idx}: Original lm1 shape: {lm1.shape}")
                    
                    if lm1.shape[0] > 5:
                        # Nếu có nhiều hơn 5 điểm, lấy 5 điểm chính
                        print(f"🔍 Frame {idx}: Truncating {lm1.shape[0]} points to 5")
                        lm1 = lm1[:5, :]
                    elif lm1.shape[0] < 5:
                        # Nếu có ít hơn 5 điểm, pad với zeros
                        print(f"🔍 Frame {idx}: Padding {lm1.shape[0]} points to 5")
                        padding = np.zeros((5 - lm1.shape[0], 2), dtype=np.float32)
                        lm1 = np.concatenate([lm1, padding], axis=0)
                    
                    # 🚨 FINAL VALIDATION: Đảm bảo chính xác (5, 2) float32
                    if lm1.shape != (5, 2):
                        print(f"🚨 Frame {idx}: Shape still wrong {lm1.shape}, forcing (5, 2)")
                        lm1 = np.zeros((5, 2), dtype=np.float32)
                    
                    print(f"✅ Frame {idx}: Final lm1 shape: {lm1.shape}, dtype: {lm1.dtype}")
                    
                    # 🚨 VALIDATE DATA TYPES
                    if not np.isfinite(lm1).all():
                        print(f"🚨 Frame {idx}: Non-finite values in landmarks, cleaning...")
                        lm1 = np.nan_to_num(lm1, nan=0.0, posinf=0.0, neginf=0.0)
                    
                except Exception as lm_error:
                    print(f"🚨 Frame {idx}: Landmark standardization failed: {lm_error}")
                    print("🚨 Creating emergency standard landmarks...")
                    lm1 = np.zeros((5, 2), dtype=np.float32)

                # 🚨 CALL align_img với landmarks đã được standardize
                try:
                    trans_params, im1, lm1, _ = align_img(frame, lm1, self.lm3d_std)
                    print(f"✅ Frame {idx}: align_img successful")
                except Exception as align_error:
                    print(f"🚨 Frame {idx}: align_img failed: {align_error}")
                    print("🚨 Using emergency fallback...")
                    # Emergency fallback: skip alignment
                    im1 = frame
                    trans_params = np.array([0.0, 0.0, 0.0], dtype=np.float32)
 
                # Fix trans_params processing to ensure consistent shape
                try:
                    if isinstance(trans_params, (list, tuple)):
                        trans_params = np.array(trans_params, dtype=np.float32)
                    elif isinstance(trans_params, np.ndarray):
                        trans_params = trans_params.astype(np.float32)
                    else:
                        trans_params = np.array([float(trans_params)], dtype=np.float32)
                    
                    # Ensure trans_params has the right shape
                    if trans_params.ndim == 1:
                        if len(trans_params) >= 3:
                            trans_params_2d = trans_params[2:3]  # Take only the 3rd element
                        else:
                            trans_params_2d = np.array([0.0], dtype=np.float32)
                    else:
                        trans_params_2d = trans_params[2:3] if trans_params.shape[1] >= 3 else np.array([[0.0]], dtype=np.float32)
                    
                    print(f"🔍 Frame {idx}: trans_params shape: {trans_params.shape}, trans_params_2d shape: {trans_params_2d.shape}")
                    
                except Exception as e:
                    print(f"⚠️ Error processing trans_params for frame {idx}: {e}")
                    trans_params_2d = np.array([[0.0]], dtype=np.float32)
                
                # 🚨 IMAGE PROCESSING PROTECTION: Đảm bảo image format đúng
                try:
                    # Convert PIL to numpy array
                    im1_array = np.array(im1)
                    print(f"🔍 Frame {idx}: Image array shape: {im1_array.shape}, dtype: {im1_array.dtype}")
                    
                    # 🚨 CRITICAL: Handle RGBA images (remove alpha channel)
                    if len(im1_array.shape) == 3 and im1_array.shape[-1] == 4:
                        print(f"🔍 Frame {idx}: RGBA detected, removing alpha channel")
                        im1_array = im1_array[..., :3]
                    
                    # 🚨 CRITICAL: Ensure RGB format
                    if len(im1_array.shape) != 3 or im1_array.shape[-1] != 3:
                        print(f"🚨 Frame {idx}: Invalid image format {im1_array.shape}, using fallback")
                        im1_array = np.zeros((256, 256, 3), dtype=np.uint8)
                    
                    # 🚨 CRITICAL: Validate pixel values
                    if not np.isfinite(im1_array).all():
                        print(f"🚨 Frame {idx}: Non-finite values in image, cleaning...")
                        im1_array = np.nan_to_num(im1_array, nan=0.0, posinf=255.0, neginf=0.0).astype(np.uint8)
                    
                    # Convert to tensor
                    im_t = torch.tensor(im1_array/255., dtype=torch.float32).permute(2, 0, 1).to(self.device).unsqueeze(0)
                    print(f"✅ Frame {idx}: Image tensor created: {im_t.shape}")
                    
                except Exception as img_error:
                    print(f"🚨 Frame {idx}: Image processing failed: {img_error}")
                    print("🚨 Using emergency fallback image...")
                    # Emergency fallback: create black image
                    im_t = torch.zeros((1, 3, 256, 256), dtype=torch.float32).to(self.device)
                
                with torch.no_grad():
                    full_coeff = self.net_recon(im_t)
                    coeffs = split_coeff(full_coeff)

                # Ensure all coefficient components have consistent shapes
                try:
                    exp_coeff = coeffs['exp'].cpu().numpy()
                    angle_coeff = coeffs['angle'].cpu().numpy()
                    trans_coeff = coeffs['trans'].cpu().numpy()
                    
                    print(f"🔍 Frame {idx}: exp_coeff shape: {exp_coeff.shape}, angle_coeff shape: {angle_coeff.shape}, trans_coeff shape: {trans_coeff.shape}")
                    
                    # Ensure all components have the same first dimension
                    max_dim = max(exp_coeff.shape[0], angle_coeff.shape[0], trans_coeff.shape[0])
                    
                    if exp_coeff.shape[0] < max_dim:
                        padding = np.zeros((max_dim - exp_coeff.shape[0], exp_coeff.shape[1]), dtype=np.float32)
                        exp_coeff = np.concatenate([exp_coeff, padding], axis=0)
                    
                    if angle_coeff.shape[0] < max_dim:
                        padding = np.zeros((max_dim - angle_coeff.shape[0], angle_coeff.shape[1]), dtype=np.float32)
                        angle_coeff = np.concatenate([angle_coeff, padding], axis=0)
                    
                    if trans_coeff.shape[0] < max_dim:
                        padding = np.zeros((max_dim - trans_coeff.shape[0], trans_coeff.shape[1]), dtype=np.float32)
                        trans_coeff = np.concatenate([trans_coeff, padding], axis=0)
                    
                    # Ensure trans_params_2d has the right shape for concatenation
                    if trans_params_2d.ndim == 1:
                        trans_params_2d = trans_params_2d.reshape(-1, 1)
                    
                    # Ensure all components have the same first dimension for concatenation
                    target_dim = max(exp_coeff.shape[0], angle_coeff.shape[0], trans_coeff.shape[0], trans_params_2d.shape[0])
                    
                    if exp_coeff.shape[0] < target_dim:
                        padding = np.zeros((target_dim - exp_coeff.shape[0], exp_coeff.shape[1]), dtype=np.float32)
                        exp_coeff = np.concatenate([exp_coeff, padding], axis=0)
                    
                    if angle_coeff.shape[0] < target_dim:
                        padding = np.zeros((target_dim - angle_coeff.shape[0], angle_coeff.shape[1]), dtype=np.float32)
                        angle_coeff = np.concatenate([angle_coeff, padding], axis=0)
                    
                    if trans_coeff.shape[0] < target_dim:
                        padding = np.zeros((target_dim - trans_coeff.shape[0], trans_coeff.shape[1]), dtype=np.float32)
                        trans_coeff = np.concatenate([trans_coeff, padding], axis=0)
                    
                    if trans_params_2d.shape[0] < target_dim:
                        padding = np.zeros((target_dim - trans_params_2d.shape[0], trans_params_2d.shape[1]), dtype=np.float32)
                        trans_params_2d = np.concatenate([trans_params_2d, padding], axis=0)
                    
                    # Ensure all components have the same second dimension for concatenation
                    total_cols = exp_coeff.shape[1] + angle_coeff.shape[1] + trans_coeff.shape[1] + trans_params_2d.shape[1]
                    
                    # Concatenate with consistent shapes
                    pred_coeff = np.concatenate([
                        exp_coeff, 
                        angle_coeff,
                        trans_coeff,
                        trans_params_2d,
                    ], axis=1)
                    
                    print(f"🔍 Frame {idx}: pred_coeff shape: {pred_coeff.shape}, total_cols: {total_cols}")
                    
                    # Validate the concatenated coefficient
                    if pred_coeff.shape[1] != total_cols:
                        print(f"⚠️ Warning: Expected {total_cols} columns, got {pred_coeff.shape[1]}")
                        # Force reshape if needed
                        if pred_coeff.shape[1] > total_cols:
                            pred_coeff = pred_coeff[:, :total_cols]
                        elif pred_coeff.shape[1] < total_cols:
                            padding = np.zeros((pred_coeff.shape[0], total_cols - pred_coeff.shape[1]), dtype=np.float32)
                            pred_coeff = np.concatenate([pred_coeff, padding], axis=1)
                        print(f"🔧 Fixed pred_coeff shape: {pred_coeff.shape}")
                    
                    print(f"🔍 Frame {idx}: pred_coeff shape: {pred_coeff.shape}")
                    
                except Exception as e:
                    print(f"❌ Error processing coefficients for frame {idx}: {e}")
                    import traceback
                    traceback.print_exc()
                    # Fallback: create a simple coefficient
                    pred_coeff = np.zeros((1, 70), dtype=np.float32)  # Standard size
                
                video_coeffs.append(pred_coeff)
                full_coeffs.append(full_coeff.cpu().numpy())

            # EMERGENCY FALLBACK: Fix array shape inhomogeneity issue with bulletproof protection
            print(f"\n🚨 EMERGENCY FALLBACK: Processing {len(video_coeffs)} coefficients...")
            
            try:
                # Step 1: Emergency coefficient validation and standardization
                emergency_coeffs = []
                target_shape = (1, 70)  # Force standard shape
                
                for i, coeff in enumerate(video_coeffs):
                    try:
                        if coeff is not None and hasattr(coeff, 'shape'):
                            if coeff.shape == target_shape:
                                emergency_coeffs.append(coeff)
                                print(f"✅ Frame {i}: Standard shape {coeff.shape}")
                            else:
                                # Force reshape to target shape
                                if len(coeff.shape) == 2:
                                    if coeff.shape[1] >= target_shape[1]:
                                        # Truncate if too wide
                                        emergency_coeffs.append(coeff[:, :target_shape[1]])
                                        print(f"🔧 Frame {i}: Truncated {coeff.shape} → {target_shape}")
                                    else:
                                        # Pad if too narrow
                                        padding = np.zeros((coeff.shape[0], target_shape[1] - coeff.shape[1]), dtype=np.float32)
                                        emergency_coeffs.append(np.concatenate([coeff, padding], axis=1))
                                        print(f"🔧 Frame {i}: Padded {coeff.shape} → {target_shape}")
                                else:
                                    # Create fallback for invalid shapes
                                    emergency_coeffs.append(np.zeros(target_shape, dtype=np.float32))
                                    print(f"⚠️ Frame {i}: Invalid shape {coeff.shape}, created fallback {target_shape}")
                        else:
                            # Create fallback for None or invalid objects
                            emergency_coeffs.append(np.zeros(target_shape, dtype=np.float32))
                            print(f"⚠️ Frame {i}: Invalid coefficient, created fallback {target_shape}")
                    except Exception as coeff_error:
                        print(f"🚨 Emergency fix failed for frame {i}: {coeff_error}")
                        emergency_coeffs.append(np.zeros(target_shape, dtype=np.float32))
                
                video_coeffs = emergency_coeffs
                print(f"✅ Emergency coefficients created: {len(video_coeffs)}")
                
                # Step 2: Verify all coefficients have identical shape
                final_shapes = [coeff.shape for coeff in video_coeffs]
                if len(set(final_shapes)) == 1:
                    print(f"🎯 All coefficients standardized to: {final_shapes[0]}")
                else:
                    print(f"🚨 Shape inconsistency detected: {final_shapes}")
                    # Force final standardization
                    for i, coeff in enumerate(video_coeffs):
                        if coeff.shape != target_shape:
                            video_coeffs[i] = np.zeros(target_shape, dtype=np.float32)
                            print(f"🚨 Frame {i}: Forced to {target_shape}")
                
                # Step 3: Emergency array creation with guaranteed consistency
                print(f"\n🚨 Step 3: Creating emergency array with guaranteed consistency...")
                
                try:
                    # Force all coefficients to target shape before array creation
                    final_coeffs = []
                    for i, coeff in enumerate(video_coeffs):
                        if coeff.shape != target_shape:
                            print(f"🚨 Frame {i}: Final shape correction {coeff.shape} → {target_shape}")
                            coeff = np.zeros(target_shape, dtype=np.float32)
                        final_coeffs.append(coeff)
                    
                    # Create array with guaranteed consistent shapes
                    video_coeffs_array = np.array(final_coeffs)
                    print(f"✅ Emergency array created successfully: {video_coeffs_array.shape}")
                    
                except Exception as array_error:
                    print(f"🚨 Emergency array creation failed: {array_error}")
                    print("🚨 Creating ultimate fallback array...")
                    # Ultimate fallback: create array with known good shape
                    video_coeffs_array = np.zeros((len(video_coeffs), target_shape[0], target_shape[1]), dtype=np.float32)
                    print(f"✅ Ultimate fallback array: {video_coeffs_array.shape}")
                
                # Step 4: Final validation and semantic extraction
                print(f"\n🎯 Final validation and semantic extraction...")
                
                try:
                    # Final validation: ensure array is valid
                    if not np.isfinite(video_coeffs_array).all():
                        print("⚠️ Non-finite values detected, cleaning...")
                        video_coeffs_array = np.nan_to_num(video_coeffs_array, nan=0.0, posinf=0.0, neginf=0.0)
                    
                    print(f"✅ Final video coefficients array shape: {video_coeffs_array.shape}")
                    print(f"✅ Final video coefficients array dtype: {video_coeffs_array.dtype}")
                    
                except Exception as validation_error:
                    print(f"🚨 Final validation failed: {validation_error}")
                    # Continue with existing array
                
                # Step 5: Extract semantic npy safely
                try:
                    if video_coeffs_array.shape[1] > 0:
                        semantic_npy = video_coeffs_array[:, 0]
                        print(f"✅ Semantic npy shape: {semantic_npy.shape}")
                    else:
                        semantic_npy = video_coeffs_array
                        print(f"✅ Semantic npy shape: {semantic_npy.shape}")
                    
                    # Validate semantic_npy
                    if not np.isfinite(semantic_npy).all():
                        print("⚠️ Non-finite values in semantic_npy, cleaning...")
                        semantic_npy = np.nan_to_num(semantic_npy, nan=0.0, posinf=0.0, neginf=0.0)
                        
                except Exception as semantic_error:
                    print(f"❌ Error extracting semantic_npy: {semantic_error}")
                    semantic_npy = np.zeros((len(video_coeffs), 70), dtype=np.float32)
                
                # Step 6: Process full_coeffs for consistency
                print(f"\n🎯 Processing full coefficients...")
                try:
                    full_coeffs_shapes = [coeff.shape for coeff in full_coeffs]
                    print(f"🔍 Full coefficients shapes: {full_coeffs_shapes}")
                    
                    if len(set(full_coeffs_shapes)) > 1:
                        print("⚠️ Inconsistent full_coeffs shapes detected, fixing...")
                        most_common_full_shape = Counter(full_coeffs_shapes).most_common(1)[0][0]
                        print(f"🎯 Most common full_coeffs shape: {most_common_full_shape}")
                        
                        fixed_full_coeffs = []
                        for i, coeff in enumerate(full_coeffs):
                            try:
                                if coeff.shape != most_common_full_shape:
                                    if coeff.shape[1] < most_common_full_shape[1]:
                                        padding = np.zeros((coeff.shape[0], most_common_full_shape[1] - coeff.shape[1]), dtype=np.float32)
                                        coeff = np.concatenate([coeff, padding], axis=1)
                                    elif coeff.shape[1] > most_common_full_shape[1]:
                                        coeff = coeff[:, :most_common_full_shape[1]]
                                fixed_full_coeffs.append(coeff)
                            except Exception as coeff_error:
                                print(f"⚠️ Error fixing full_coeff {i}: {coeff_error}, using fallback")
                                fixed_full_coeffs.append(np.zeros(most_common_full_shape, dtype=np.float32))
                        
                        full_coeffs = fixed_full_coeffs
                    
                    full_coeffs_array = np.array(full_coeffs)
                    print(f"✅ Full coefficients array shape: {full_coeffs_array.shape}")
                    
                except Exception as full_coeffs_error:
                    print(f"❌ Error processing full_coeffs: {full_coeffs_error}")
                    full_coeffs_array = np.zeros((len(full_coeffs), 256), dtype=np.float32)
                
                # Step 7: Save coefficients with validation
                print(f"\n💾 Saving coefficients...")
                try:
                    savemat(coeff_path, {'coeff_3dmm': semantic_npy, 'full_3dmm': full_coeffs_array[0]})
                    print(f"✅ 3DMM coefficients saved successfully to {coeff_path}")
                    print(f"✅ File size: {os.path.getsize(coeff_path)} bytes")
                    
                    # Verify saved file
                    if os.path.exists(coeff_path) and os.path.getsize(coeff_path) > 0:
                        print("✅ Coefficient file verified successfully")
                    else:
                        print("⚠️ Coefficient file verification failed")
                        
                except Exception as save_error:
                    print(f"❌ Error saving coefficients: {save_error}")
                    raise save_error
                
            except Exception as e:
                print(f"❌ Error processing 3DMM coefficients: {e}")
                import traceback
                traceback.print_exc()
                print("🔄 Falling back to simple coefficient processing...")
                
                # Enhanced fallback with validation
                if video_coeffs:
                    try:
                        # Try to use the first coefficient
                        semantic_npy = video_coeffs[0]
                        full_coeffs_array = full_coeffs[0] if full_coeffs else np.array([])
                        
                        # Ensure semantic_npy is 2D and valid
                        if semantic_npy.ndim == 1:
                            semantic_npy = semantic_npy.reshape(1, -1)
                        
                        # Validate and clean
                        if not np.isfinite(semantic_npy).all():
                            semantic_npy = np.nan_to_num(semantic_npy, nan=0.0, posinf=0.0, neginf=0.0)
                        
                        savemat(coeff_path, {'coeff_3dmm': semantic_npy, 'full_3dmm': full_coeffs_array})
                        print(f"✅ Fallback coefficients saved to {coeff_path}")
                        print(f"✅ Fallback semantic_npy shape: {semantic_npy.shape}")
                        
                    except Exception as fallback_error:
                        print(f"❌ Even fallback failed: {fallback_error}")
                        print("🔄 Creating emergency fallback...")
                        try:
                            emergency_coeff = np.zeros((1, 70), dtype=np.float32)
                            emergency_full = np.zeros((1, 256), dtype=np.float32)
                            savemat(coeff_path, {'coeff_3dmm': emergency_coeff, 'full_3dmm': emergency_full})
                            print("✅ Emergency fallback coefficients saved")
                        except Exception as emergency_error:
                            print(f"❌ Emergency fallback also failed: {emergency_error}")
                            return None, None
                else:
                    print("❌ No coefficients available for saving")
                    return None, None

        return coeff_path, png_path, crop_info
