# 🚀 Deployment Guide for Obesity Prediction App

## Quick Deployment Steps

### 1. Create GitHub Repository
1. Go to [GitHub](https://github.com) and create a new repository
2. Name it something like `obesity-prediction-app`
3. Make it **public** (required for Streamlit Community Cloud free tier)
4. Don't initialize with README, .gitignore, or license (we already have these)

### 2. Connect Local Repository to GitHub
```bash
# Add your GitHub repository as remote origin
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY_NAME.git

# Push to GitHub
git branch -M main
git push -u origin main
```

### 3. Deploy on Streamlit Community Cloud
1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click "New app"
4. Select your repository: `YOUR_USERNAME/YOUR_REPOSITORY_NAME`
5. Set main file path: `src/app_obesite.py`
6. Click "Deploy!"

## 📋 Pre-deployment Checklist

✅ Git repository initialized  
✅ .gitignore file created  
✅ requirements.txt configured  
✅ Streamlit config.toml set up  
✅ Initial commit made  

## 🔧 Configuration Details

- **Main app file**: `src/app_obesite.py`
- **Python version**: 3.8+ (automatically detected)
- **Dependencies**: Listed in `requirements.txt`
- **Theme**: Custom theme configured in `.streamlit/config.toml`

## 📁 Repository Structure
```
app_obesite/
├── src/
│   ├── app_obesite.py      # Main Streamlit app
│   ├── utils.py            # Utility functions
│   ├── ui_components.py    # UI components
│   └── advice_engine.py    # Advice generation
├── models/
│   └── modele_lgbm.pkl     # Trained model
├── data/
│   └── *.csv              # Dataset files
├── .streamlit/
│   └── config.toml         # Streamlit configuration
├── requirements.txt        # Python dependencies
└── README_DEPLOYMENT.md    # This file
```

## 🚨 Important Notes

1. **Repository must be public** for free Streamlit Community Cloud
2. **Model files** (~100MB) are included - ensure they're under GitHub's file size limits
3. **First deployment** may take 5-10 minutes
4. **Automatic redeployment** happens on every push to main branch

## 🔗 Useful Links

- [Streamlit Community Cloud](https://share.streamlit.io)
- [Streamlit Deployment Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [GitHub](https://github.com)

## 🆘 Troubleshooting

**If deployment fails:**
1. Check the logs in Streamlit Community Cloud
2. Verify all dependencies in requirements.txt
3. Ensure the main file path is correct: `src/app_obesite.py`
4. Check that model files are accessible

**Common issues:**
- Missing dependencies → Update requirements.txt
- File path errors → Verify relative paths in code
- Model loading errors → Check model file paths