from exm_deeplearn_lib.exmsyn_models import unet_like
from exm_deeplearn_lib.exmsyn_compile import gen_unet_batch_v2
from exm_deeplearn_lib.exmsyn_network import masked_binary_crossentropy
from exm_deeplearn_lib.exmsyn_network import masked_accuracy, masked_error_pos, masked_error_neg
from exm_deeplearn_lib.exmsyn_network import DeepNeuralNetwork
from keras.optimizers import SGD
import pickle


file_path = '# /imagedirectory'
img_mask_junk_names = [(file_path+'# RAWDATA1.nrrd', file_path+'# SYNAPSEMASKS1.nrrd'), \
    (file_path+'# RAWDATA2.nrrd',file_path+'# SYNAPSEMASKS2.nrrd'), \
    (file_path+'# RAWDATA3.nrrd', file_path+'# SYNAPSEMASKS3.nrrd')]
    
input_shape = (64,64,64)
model = unet_like(input_shape)
sgd_opti = SGD(lr=0.001, momentum=0.9, decay=0.00005, nesterov=True)
compile_args = {'optimizer':sgd_opti, 'loss':masked_binary_crossentropy, 'metrics':[masked_accuracy, masked_error_pos, masked_error_neg]}
network = DeepNeuralNetwork(model, compile_args=compile_args)

batch_sz = 16
n_gpus = 1
generator = gen_unet_batch_v2(img_mask_junk_names, crop_sz=(64,64,64), mask_sz=(24,24,24), batch_sz=batch_sz*n_gpus)
save_path = '# /savedirectory'
history = network.train_network(generator=generator, steps_per_epoch=100, epochs=3000, n_gpus=n_gpus, save_name=None)

with open(save_path+'history_rawdata_gen2_lr1e-3_sgd_batch64_steps100_epochs3000.pkl', 'wb') as f:
    pickle.dump(history.history, f)

network.save_whole_network(save_path+'# modelname')
# network.save_architecture(save_path+'unet')