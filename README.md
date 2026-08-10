# Smart Wallet API

Installation
```bash
git clone https://github.com/yewontaung/smart-wallet-api.git
cd smart-wallet-api
python -m .venv venv
.venv\Scripts\active
pip install -r requirements.txt
```

.env
```
DATABASE_URL=sqlite:///./bank.db
JWT_SECRET=your_jwt_secret
API_VERSION=1
DEMO_PASSWORD=hello
```

Runing the project
```bash
uvicorn app.main:app
```

Database seeding
```bash
python -m seeding.seeder
```

Swagger UI URL
```
http://localhost:8000/docs
```

Contribution Branch
```bash
git branch
git switch [feat/your_branch]
git pull origin [feat/your_branch]
```

Commit Guide
```bash
git branch
git status
git add [file_name]
git commit -m "feat: Add [feat_name] feature"
git push origin [feat/your_branch]
```

*you can pull request to dev branch*