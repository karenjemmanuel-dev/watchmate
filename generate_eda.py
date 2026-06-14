import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# Load data
print("Loading data...")
ratings = pd.read_csv('data/u.data', sep='\t', names=['user_id', 'movie_id', 'rating', 'timestamp'])
movies = pd.read_csv('data/u.item', sep='|', encoding='latin-1',
                     names=['movie_id', 'title', 'release_date', 'video_release', 'imdb_url',
                            'unknown', 'Action', 'Adventure', 'Animation', 'Children', 'Comedy',
                            'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
                            'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western'])

data = pd.merge(ratings, movies[['movie_id', 'title']], on='movie_id')

# Create simple HTML report
html = f"""
<html>
<head>
    <title>WatchMate EDA Report</title>
    <style>
        body {{ font-family: Arial; margin: 40px; background: #f5f5f5; }}
        h1 {{ color: #1f77b4; }}
        h2 {{ color: #1f77b4; margin-top: 30px; }}
        table {{ border-collapse: collapse; width: 100%; background: white; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #1f77b4; color: white; }}
        .stat {{ background: white; padding: 20px; margin: 10px 0; border-radius: 5px; }}
    </style>
</head>
<body>
    <h1>WatchMate MovieLens Exploratory Data Analysis</h1>
    <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    
    <h2>Dataset Overview</h2>
    <div class="stat">
        <p><b>Total Ratings:</b> {len(ratings):,}</p>
        <p><b>Total Movies:</b> {len(movies):,}</p>
        <p><b>Total Users:</b> {ratings['user_id'].nunique()}</p>
        <p><b>Rating Range:</b> {ratings['rating'].min()} to {ratings['rating'].max()}</p>
    </div>
    
    <h2>Rating Distribution</h2>
    <div class="stat">
        <table>
            <tr><th>Rating</th><th>Count</th><th>Percentage</th></tr>
"""

for rating in sorted(ratings['rating'].unique()):
    count = len(ratings[ratings['rating'] == rating])
    pct = (count / len(ratings)) * 100
    html += f"            <tr><td>{rating}</td><td>{count:,}</td><td>{pct:.1f}%</td></tr>\n"

html += f"""
        </table>
    </div>
    
    <h2>Top 10 Most Rated Movies</h2>
    <div class="stat">
        <table>
            <tr><th>Movie Title</th><th>Number of Ratings</th></tr>
"""

top_movies = data['title'].value_counts().head(10)
for movie, count in top_movies.items():
    html += f"            <tr><td>{movie}</td><td>{count}</td></tr>\n"

html += f"""
        </table>
    </div>
    
    <h2>Data Quality</h2>
    <div class="stat">
        <p><b>Missing Values:</b> {data.isnull().sum().sum()} (0 is good)</p>
        <p><b>Duplicate Ratings:</b> {data.duplicated(subset=['user_id', 'movie_id']).sum()} (0 is good)</p>
        <p><b>Average Rating:</b> {ratings['rating'].mean():.2f}</p>
        <p><b>Median Rating:</b> {ratings['rating'].median():.2f}</p>
    </div>
    
</body>
</html>
"""

with open('outputs/eda_report.html', 'w') as f:
    f.write(html)

print("✓ EDA report saved to outputs/eda_report.html")