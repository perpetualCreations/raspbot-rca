from pyAudioAnalysis import audioTrainTest as aT
aT.extract_features_and_train(["training-audio/ambient","training-audio/rustling"], 1.0, 1.0, aT.shortTermWindow, aT.shortTermStep, "svm", "svmSMtemp", False)
aT.file_classification("training-audio/2.wav", "svmSMtemp","svm")
