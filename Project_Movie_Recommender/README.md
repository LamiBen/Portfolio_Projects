# Movie Recommender: Baselines vs Matrix Factorisation

**Question:** Can a matrix factorisation model predict what a user will rate a movie, and does it recommend better than simple popularity?

**Data:** The MovieLens ratings file in `Project_Movies/data/` (100,818 ratings from 610 users; every user has at least 20 ratings). Ratings run from 0.5 to 5.0.

**Method**
- Held out 20% of each user's ratings for testing, so every user appears in training.
- Built three baselines: global mean, user mean, and item (movie) mean.
- Implemented a biased matrix factorisation model from scratch with NumPy: each rating is predicted from a global mean, a user bias, a movie bias, and the dot product of 20 latent factors. Trained with stochastic gradient descent and L2 regularisation.
- Evaluated two things: rating prediction (RMSE and MAE on held-out ratings), and top-10 recommendation precision (share of recommended movies that the user rated 4 or higher in the test set), compared against a most-popular baseline.

**Results**

| Model | RMSE | MAE |
|---|---|---|
| Global mean | 1.051 | 0.834 |
| User mean | 0.946 | 0.739 |
| Item mean | 0.982 | 0.760 |
| Matrix factorisation | **0.872** | **0.668** |

Top-10 precision: the most-popular baseline scores **0.119**, and matrix factorisation scores **0.031**.

**Interpretation**
- Matrix factorisation is clearly better at predicting ratings than every baseline.
- It is much worse at ranking: on this data, recommending popular movies gives better top-10 lists. The model is probably over-fitting to sparse, niche movies with few ratings, and it was not tuned beyond a single setting.

**Next steps**
- Tune the number of factors and the regularisation strength on a validation split, not the test set.
- Evaluate ranking with a method designed for it, such as implicit-feedback ALS on liked / not-liked data.
- Add a cold-start strategy for new users and new movies.

**Files**
- `recommender.py`: data split, baselines, the model, and both evaluations (`python recommender.py`, about 25 seconds)
- `figures/model_comparison.png`: RMSE by model and training RMSE by epoch

**Note:** Run from this folder; the script reads the ratings from `../Project_Movies/data/`.
