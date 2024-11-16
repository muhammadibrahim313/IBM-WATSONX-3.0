def run_watson_granite(user_input):
    from ibm_watsonx_ai import Credentials
    from ibm_watsonx_ai.foundation_models import ModelInference
    from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams
    from ibm_watsonx_ai.foundation_models.utils.enums import ModelTypes, DecodingMethods

    # Setting up the model parameters
    gen_params = {
        GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
        GenParams.TEMPERATURE: 0.8,
        GenParams.MIN_NEW_TOKENS: 10,
        GenParams.MAX_NEW_TOKENS: 1024
    }

    # Initialize the model inference
    model_inference = ModelInference(
        model_id="name_of_model",
        params=gen_params,
        credentials=Credentials(
            api_key="apikey",
            url="endpoint_url"
        ),
        project_id="your_project_id"
    )

    # Define the system's role with parameters
    system_prompt = (
        "You are an agriculture expert who predicts the crop yield for a user based on the parameters.\n"
        "When the user asks a question, provide a response based only on the input provided.\n"
        "You will also suggests the crops that are popular in that area or that can have higher yields and higher profits based on parameters\n"
        """
        Results:
                information about the predicted yield
        Possible Crops:
                information about the suitable crops
           """
    )

    # Combine system prompt with user input
    complete_prompt =  system_prompt +" "+user_input

    # Generate response from the model
    response = model_inference.generate(complete_prompt)
    results = response.get('results', [])

    del model_inference

    # Extract the generated text from the response
    generated_texts = [item.get('generated_text') for item in results]

    return generated_texts

# Execute the call
prompt = "I have a 50-acre farm in Iowa with loam soil. What crop should I plant this season?"
response = run_watson_granite(prompt)
print(response)
