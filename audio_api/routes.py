from flask import jsonify, send_file, send_from_directory, request
import os
import traceback

def configure_routes(app):

    @app.route('/')
    def index():
        return render_template('index.html')

    @app.route('/get_audio_content/<filename>', methods=['GET'])
    def get_audio_content(filename):
        # Assuming the audio files are stored in a directory named 'audio_files'
        audio_path = os.path.join(app.root_path, 'demo_audio', filename)
        return send_file(audio_path, as_attachment=True)

    @app.route('/demo_audio/<path:filename>')
    def serve_audio(filename):
        try:
            return send_from_directory('demo_audio', filename)
        except Exception as e:
            traceback.print_exc()  # Print the traceback for debugging
            return str(e), 500  # Return the error message and status code

    @app.route('/get_files')
    def get_files():
        
        # Assuming the audio files are stored in a directory named 'audio_files'
        folder_path = 'demo_audio'

        # Get the list of files in the directory
        files = os.listdir(folder_path)
        return jsonify(files=files)



    @app.route('/transcribe', methods=['POST'])
    def transcribe_audio_onnx():
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file found'}), 400

        audio_file = request.files['audio']
        
        audio_file = secure_filename(audio_file.filename)
        file_path = os.path.join('/workspace/advanced-speech-LLM-demo/asr-nl_onnx/demo_audio', audio_file)
        
        selected_model = request.form.get('model_name')  # Get the selected model name from the request
        selected_language = request.form.get('language_id')  # Get the selected model name from the request
        
        print("SELECTED LANGUAGE: ", selected_language)
        
        if selected_language == "EN":
            
            if selected_model == "ner_emotion_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_ner, model_tokenizer_en, file_path)
            
            elif selected_model == "pos_emotion_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_pos, model_tokenizer_en, file_path)
            elif selected_model == "ner_noise_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_noise, model_tokenizer_noise, file_path)

        if selected_language == "EURO":
            
            transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_euro_ner, model_tokenizer_euro, file_path)
    
        
        transcript = transcript.replace("END", " END ")
        transcript = re.sub(' +', ' ', transcript)
        return jsonify({'transcript': transcript,'token_timestamps': token_timestamps})

    @app.route('/transcribe_twilio', methods=['POST'])
    def transcribe_audio_onnx_twilio():
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file found'}), 400

        audio_file = request.files['audio']
        
        audio_file = secure_filename(audio_file.filename)
        file_path = os.path.join('/workspace/advanced-speech-LLM-demo/twilio/user_audio', audio_file)
        
        selected_model = request.form.get('model_name')  # Get the selected model name from the request
        selected_language = request.form.get('language_id')  # Get the selected model name from the request
        
        print("SELECTED LANGUAGE: ", selected_language)
        
        if selected_language == "EN":
            
            if selected_model == "ner_emotion_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_ner, model_tokenizer_en, file_path)
            
            elif selected_model == "pos_emotion_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_pos, model_tokenizer_en, file_path)
            elif selected_model == "ner_noise_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_noise, model_tokenizer_noise, file_path)

        if selected_language == "EURO":
            
            transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_euro_ner, model_tokenizer_euro, file_path)
    
        
        transcript = transcript.replace("END", " END ")
        transcript = re.sub(' +', ' ', transcript)
        return jsonify({'transcript': transcript,'token_timestamps': token_timestamps})



    @app.route('/transcribe-s2s', methods=['POST'])
    def transcribe_audio_onnx_s2s():
        print("-----------------------New-Turn----------------------")
        if 'audio' not in request.files:
            return jsonify({'error': 'No audio file found'}), 400

        audio_file = request.files['audio']
        print("Audio-File-Input:", audio_file)
        audio_file = secure_filename(audio_file.filename)
        file_path = os.path.join('/workspace/advanced-speech-LLM-demo/voice-assistant/static/audio/input', audio_file)

        try:
            data = request.form

        except Exception as e:
            print("Error:", str(e))
            return "Error: " + str(e), 500  # Return an error response with a 500 status code

        selected_model = data.get('model_name')  # Get the selected model name from the request
        selected_language = data.get('language_id')  # Get the selected model name from the request
        
        print("SELECTED LANGUAGE: ", selected_language)
        
        print("SELECTED MODEL", selected_model)

        if selected_language == "EN":
            
            if selected_model == "ner_emotion_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_ner, model_tokenizer_en, file_path)
            
            elif selected_model == "pos_emotion_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_pos, model_tokenizer_en, file_path)
            elif selected_model == "ner_noise_commonvoice":
                transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_en_noise, model_tokenizer_noise, file_path)

        if selected_language == "EURO":
            
            transcript, token_timestamps = infer_audio_file(filterbank_featurizer, ort_session_euro_ner, model_tokenizer_euro, file_path)
    
        
        transcript = transcript.replace("END", " END ")
        transcript = re.sub(' +', ' ', transcript)
        print("Generated tokens: ", transcript)
        return jsonify({'transcript': transcript,'token_timestamps': token_timestamps})
    
    
    # Endpoint for clearing conversation history
    @app.route('/clear_history', methods=['POST'])
    def clear_history():
        global conversation_history
        print("Conversation History")
        print(conversation_history)
        conversation_history = []
        print("Clearing Conversation History")
        print(conversation_history)
        return jsonify({'success': True})

    def clean_tags(input_text):
        input_text = input_text.split()
        new_sent = []
        for word in input_text:
            if "NER_" not in word and "END" not in word and "EMOTION_" not in word:
                new_sent.append(word)

        return " ".join(new_sent)

    @app.route('/llm_response', methods=['POST'])
    def llm_response():
        
        global conversation_history

        data = request.form
        input_text = data.get('content')  # Access the received text input
        print("Input Text: ", input_text)
        #input_text  = "<s> [INST] Organize text into html table which has three columns with unique NER_<type>, possibly multiple values (END token ends the entity value after NER_<type> which is the start token) and third column for EMOTION_<type> [/INST] " + input_text +" </s> [INST] Give me the table with slot name and values."
        emotion = data.get('emotion')

        input_text = clean_tags(input_text)
        
        conversation_history.append({"role": "user", "content": input_text, "emotion": emotion})

        text = llm_class.generate_response(input_text, emotion, conversation_history)

        print("LLM text", text)
        text = text.split("assistant")[1].strip().rstrip()
        
        
        conversation_history.append({"role": "system", "content": text, "emotion": emotion})

        


        return jsonify({'response': text,"input_text": input_text})

    @app.route('/llm_response_openai', methods=['POST'])
    def llm_response_openai():
        
        global conversation_history

        data = request.form
        input_text = data.get('content')  # Access the received text input
        print("Input text: ", input_text)
        #input_text  = "<s> [INST] Organize text into html table which has three columns with unique NER_<type>, possibly multiple values (END token ends the entity value after NER_<type> which is the start token) and third column for EMOTION_<type> [/INST] " + input_text +" </s> [INST] Give me the table with slot name and values."
        emotion = data.get('emotion')

        input_text = clean_tags(input_text) + ' {emotionalstate: '+emotion+'}'
        print("Clean text: ", input_text)

        conversation_history.append({"role": "user", "content": input_text, "emotion": emotion})

        openai.api_key = "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"

        temperature = 0.1
        
        instructions = "I understand role, content and emotional state to give a empethatic reply like a real human"

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Choose the appropriate model
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": input_text}
            ],
            temperature=temperature,
            max_tokens=150
        )
        
        print(response)
        
        
        text = response['choices'][0]['message']['content']

        #print("LLM text", text)
        #text = text.split("assistant")[1].strip().rstrip()
        
        
        conversation_history.append({"role": "system", "content": text, "emotion": emotion})

        


        return jsonify({'response': text,"input_text": input_text})


    @app.route('/llm_response_tensorrt', methods=['POST'])
    def llm_response_tensorrt():
        
        global conversation_history

        data = request.form
        input_text = data.get('content')  # Access the received text input
        print("Input text: ", input_text)
        #input_text  = "<s> [INST] Organize text into html table which has three columns with unique NER_<type>, possibly multiple values (END token ends the entity value after NER_<type> which is the start token) and third column for EMOTION_<type> [/INST] " + input_text +" </s> [INST] Give me the table with slot name and values."
        #emotion = data.get('emotion')

        #input_text = clean_tags(input_text) + ' {emotionalstate: '+emotion+'}'
        print("Clean text: ", input_text)

        conversation_history.append({"role": "user", "content": input_text})


        temperature = 0.1
        
        instructions = "I understand role, content and emotional state to give a empethatic reply like a real human"

        response = get_llm_reply(llm_model, runner, input_text, args)
        
        response = response.split('<|Bot|>:"\nOutput [Text 0 Beam 0]:')[-1]

        #print("LLM text", text)
        #text = text.split("assistant")[1].strip().rstrip()
        
        
        conversation_history.append({"role": "system", "content": response})

        


        return jsonify({'response': response,"input_text": input_text})


    @app.route('/generate_audio_cloning', methods=['POST'])
    def generate_audio():
        try:
            data = request.form
            text_to_convert = data.get('text_to_convert')  # Get the text to convert from the request
            output_filename = data.get('output_filename')  # Get the desired output filename from the request

            # Generate audio from the provided text
            #audio_file_path = generate_audio_from_text(text_to_convert, output_filename)

            tts_model.tts_to_file_cloning(text_to_convert, speaker_wav_folder, language, output_filename)

            return jsonify({'audio_file_path': audio_file_path})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    @app.route('/generate_audio_gtts', methods=['POST'])
    def generate_audio_gtts():
        # Create a gTTS object with the text
        data = request.form
        text_to_convert = data.get('text_to_convert')  # Get the text to convert from the request
        output_filename = data.get('output_filename')  # Get the desired output filename from the request

        tts = gTTS(text_to_convert)

        # Save the audio to the specified file
        tts.save(output_filename)
        
        return jsonify({'audio_file_path': output_filename})

    @app.route('/process_llm', methods=['POST'])
    def process_llm():
        
        input_text = request.form.get('text')  # Access the received text input
        
        #input_text  = "<s> [INST] Organize text into html table which has three columns with unique NER_<type>, possibly multiple values (END token ends the entity value after NER_<type> which is the start token) and third column for EMOTION_<type> [/INST] " + input_text +" </s> [INST] Give me the table with slot name and values."
        
        selected_model = request.form.get('model_name')
        
        token_timestamps = request.form.get('timestamps')
        #print("token_timestamps: ", token_timestamps)
        # Run LLM function on the input_text (perform the necessary processing here)
        #processed_output = llm(input_text, temperature=0.001)  # Replace with your LLM function
        #processed_output = processed_output.replace("\n", "")
        #processed_output = processed_output.replace("||", "\n")
        
        if selected_model == "ner_emotion_commonvoice":
            processed_output = extract_entities(input_text, token_timestamps, tag="NER")
        else:
            processed_output = extract_entities(input_text, token_timestamps, tag="POS")
        
        print("Processed Output", processed_output)
        return jsonify({'processed_output': processed_output})


    @app.route('/process_llm-s2s', methods=['POST'])
    def process_llm_s2s():
        
        data = request.form

        input_text = data.get('text')  # Access the received text input
        
        #input_text  = "<s> [INST] Organize text into html table which has three columns with unique NER_<type>, possibly multiple values (END token ends the entity value after NER_<type> which is the start token) and third column for EMOTION_<type> [/INST] " + input_text +" </s> [INST] Give me the table with slot name and values."
        
        selected_model = data.get('model_name')
        
        token_timestamps = data.get('timestamps')
        token_timestamps = json.loads(token_timestamps)
        #print("token_timestamps: ", token_timestamps)
        # Run LLM function on the input_text (perform the necessary processing here)
        #processed_output = llm(input_text, temperature=0.001)  # Replace with your LLM function
        #processed_output = processed_output.replace("\n", "")
        #processed_output = processed_output.replace("||", "\n")
        
        if selected_model == "ner_emotion_commonvoice":
            processed_output = extract_entities_s2s(input_text, token_timestamps, tag="NER")
        else:
            processed_output = extract_entities_s2s(input_text, token_timestamps, tag="POS")
        
        return jsonify({'processed_output': processed_output})
    
