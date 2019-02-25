class ManyMany:
    def write(model1, model2):
        if model1.saved and model2.saved:
            print("Successful through-table fake write")
        else:
            print("Cannot save many to many relationship if both models are not saved")
