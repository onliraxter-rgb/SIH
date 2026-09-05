@echo off
echo ============================================
echo   VoiceGuard -- Installing Dependencies
echo ============================================
pip install flask librosa scikit-learn numpy requests soundfile werkzeug scipy
echo.
echo ============================================
echo   Done! Now run:
echo     python generate_dataset.py   (generate fake audio)
echo     python train.py              (train the model)
echo     python app.py                (start the app)
echo ============================================
pause
