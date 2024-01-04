import pickle
import pandas as pd
import streamlit as st
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url).json()
    poster_path = data.get("poster_path")
    full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
    return full_path


def recommend(movie):
    index_ = movies[movies['title'] == movie].index[0]

    distances = sorted(list(enumerate(similarity[index_])), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_scores = []  # Store similarity scores here

    for i in distances[1:13]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

        # Calculate similarity score as a percentage
        similarity_score = (i[1]) * 100
        recommended_movie_scores.append("{:.0f}%  Match".format(similarity_score))

    return recommended_movie_names,  recommended_movie_scores, recommended_movie_posters



def extract_movie_details(movie_id):
    movie_row = movies_details[movies_details['movie_id'] == movie_id]

    if movie_row.empty:
        return "Movie details not found."

    movie_details_row = movie_row.iloc[0].to_dict()

    # Handling the 'Genres' formatting
    genres = movie_details_row.get('genres', None)
    if genres is not None:
        genres = ', '.join(genres)
        # Removing brackets and quotes
        genres = genres.strip('[]').replace("'", "")

    detail = {
        'Title': movie_details_row.get('title', None),
        'Tagline': movie_details_row.get('tagline', None),
        'Cast': movie_details_row.get('cast', None),
        'Director': movie_details_row.get('Director', None),
        'Genres': genres,  # Modified 'Genres' entry
        'Language': movie_details_row.get('original_language', None),
        'Runtime (minutes)': movie_details_row.get('runtime', None),
        'Release Year': movie_details_row.get('release_year', None)
    }

    formatted_details = ""
    for key, value in detail.items():
        if value is not None:
            formatted_details += f"{key}: <b>{value}</b> <br>"

    if not formatted_details:
        return "Movie details not found."

    return formatted_details


def add_bg_from_url():
    st.markdown(
        f"""
         <style>
         .stApp {{
             background-image: url("https://img.freepik.com/free-vector/digital-technology-background-with-blue-orange-light-effect_1017-27423.jpg?w=996&t=st=1704190963~exp=1704191563~hmac=83d9dae9f8eb76ffa167bccce92637b5840cd9e9fc9882ead57f7b051d17f886");
             background-attachment: fixed;
             background-size: cover
         }}
         </style>
         """,
        unsafe_allow_html=True
    )


add_bg_from_url()

# Inject custom CSS
st.markdown(
    """
    <style>
    .header-style {
        background-color: tomato; /* Off-white background color */
        padding: 10px; /* Padding around the header */
        border-radius: 5px; /* Rounded corners */
        text-align: center; /* Align text to center */
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Display the styled header
st.markdown('<h3 class="header-style">CONTENT  BASED  RECOMMENDATION  SYSTEM</h3>', unsafe_allow_html=True)

movies_dict = pickle.load(open('movie_list.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('similarity.pkl', 'rb'))

movies_details = pickle.load(open('movie_details.pkl', 'rb'))
movies_details = pd.DataFrame(movies_details)

movie_list = movies['title'].values
html_label = (
    '<div style="background-color: #f8f8ff; padding: 8px; border-radius: 5px; '
    'font-weight: bold;">Type or select a movie from the dropdown</div>'
)
st.markdown(html_label, unsafe_allow_html=True)

# Display the selectbox without a label
selected_movie = st.selectbox(
    "",
    movie_list
)

selected_movie_index = movies[movies['title'] == selected_movie].index[0]

if st.button('Show Recommendation'):
    # selected_movie_name = movies.iloc[selected_movie_index].title
    selected_movie_poster = fetch_poster(movies.iloc[selected_movie_index].movie_id)

    recommended_movie_names,  recommended_movie_scores, recommended_movie_posters = recommend(selected_movie)


    def colored_text(text, color, font_color='#55298F', font_weight='bold'):
        return f'<div style="background-color:{color}; color:{font_color}; font-weight:{font_weight}; padding: 5px">{text}</div>'


    # Set the background color for text
    background_color = '#E2D5F3'


    def colored_text_2(text, color, font_weight='bold'):
        return f'<div style="background-color:{color}; font-weight:{font_weight}; padding: 5px">{text}</div>'


    # Set the background color for text
    background_color_2 = '#A58BCF'  # Replace this with your desired color code


    def colored_text_3(text, color):
        return f'<div style="background-color:{color}; padding: 5px">{text}</div>'


    # Set the background color for text
    background_color_3 = '#E2D5F3'  # Replace this with your desired color code

    # import streamlit as st

    # Displaying the image in the center
    st.markdown(f'<img src="{selected_movie_poster}" style="display: block; margin-left: auto;margin-right: auto; width: 300px;" alt="{selected_movie}"/>',unsafe_allow_html=True)

    st.write("")

    # Creating a layout with columns to align the expander dropdown and image
    col1, col2, col3 = st.columns([1, 1, 1])  # Adjust column ratios as needed

    with col1:
        pass  # This column will be empty to create space

    with col2:
        with st.expander(f":orange[**{selected_movie}** Details]"):
            details_x = extract_movie_details(movies[movies['title'] == selected_movie].iloc[0].movie_id)
            st.markdown(f"<div style='width: 300px;'>{colored_text_3(details_x, background_color_3)}</div>",
                        unsafe_allow_html=True)

    with col3:
        pass  # This column will be empty to create space

    st.write("")
    st.write("")
    st.write("")  # Add an empty line for spacing
    st.markdown(
        f'<h3 style="color: black; background-color: #F0F0F0; padding: 8px; border-radius: 5px;font-size: 18px;">'
        f'Since you watched {selected_movie}, we recommend these movies for you'
        f'</h3>',
        unsafe_allow_html=True
    )

    st.write("")


# displaying the recommended movies
    col_count = 4
    row_count = 3

    for i in range(row_count):
        cols = st.columns(col_count)
        for j in range(col_count):
            index = i * col_count + j

            with cols[j]:
                st.markdown(colored_text(recommended_movie_names[index], background_color), unsafe_allow_html=True)
                st.markdown(colored_text_2(recommended_movie_scores[index], background_color_2), unsafe_allow_html=True)
                st.image(recommended_movie_posters[index])
                with st.expander(f":green[**{recommended_movie_names[index]}** Details]"):
                    details = extract_movie_details(
                        movies[movies['title'] == recommended_movie_names[index]].iloc[0].movie_id)
                    st.markdown(colored_text_3(details, background_color_3), unsafe_allow_html=True)

# streamlit run app.py
