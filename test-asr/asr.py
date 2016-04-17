class MonoDecoder(object):
    def __init__(self, words_path, model_path, hclg_path):
        self.words_path = words_path
        self.model_path = model_path
        self.hclg_path = hclg_path

    def make_features(self, wave_path):
        # return feature dir
        pass

    def decode(self, wave_path, feature_path):
        # return decoded text
        pass
