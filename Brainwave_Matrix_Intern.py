import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report
import joblib  # for saving/loading models

# Load datasets (update paths if needed)
fake_df = pd.read_csv(r"C:\Users\DELL\fake-and-real-news-dataset\Fake.csv")
real_df = pd.read_csv(r"C:\Users\DELL\fake-and-real-news-dataset\True.csv")

# Add labels
fake_df['label'] = 'FAKE'
real_df['label'] = 'REAL'

# Combine datasets and shuffle
df = pd.concat([fake_df, real_df], ignore_index=True)
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Use only relevant columns
df = df[['text', 'label']]

# Split data into features and target
X = df['text']
y = df['label']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Initialize vectorizer
tfidf = TfidfVectorizer(stop_words='english', max_df=0.7)

# Fit-transform train, transform test
X_train_tfidf = tfidf.fit_transform(X_train)
X_test_tfidf = tfidf.transform(X_test)

# Train model
model = LogisticRegression()
model.fit(X_train_tfidf, y_train)

# Test predictions and evaluation
y_pred = model.predict(X_test_tfidf)
print("Accuracy on test set:", accuracy_score(y_test, y_pred))
print("\nClassification Report:\n", classification_report(y_test, y_pred))

# Save model and vectorizer to disk
joblib.dump(model, "fake_news_model.joblib")
joblib.dump(tfidf, "tfidf_vectorizer.joblib")
print("Model and vectorizer saved to disk.")

# Function to load model/vectorizer and predict new text
def load_model_and_predict(text):
    model_loaded = joblib.load("fake_news_model.joblib")
    vectorizer_loaded = joblib.load("tfidf_vectorizer.joblib")
    text_tfidf = vectorizer_loaded.transform([text])
    prediction = model_loaded.predict(text_tfidf)[0]
    return prediction

# Example usage
if __name__ == "__main__":
    sample_news = "The government is planning to reduce taxes next year."
    result = load_model_and_predict(sample_news)
    print(f"\nPrediction for sample news: {result}")
