import streamlit as st
import json
from datetime import datetime

DEFAULT_BOOKS = [
    {"title": "The World As I See It", "author": "Albert Einstein", "year": 1934, "genre": "Science", "read": True},
    {"title": "Bang-e-Dra", "author": "Allama Iqbal", "year": 1924, "genre": "Poetry", "read": False}
]

def load_library():
    try:
        with open('library.json', 'r') as f:
            library = json.load(f)
            if not library:
                save_library(DEFAULT_BOOKS)
                return DEFAULT_BOOKS
            return library
    except (FileNotFoundError, json.JSONDecodeError):
        save_library(DEFAULT_BOOKS)
        return DEFAULT_BOOKS

def save_library(library):
    with open('library.json', 'w') as f:
        json.dump(library, f)

st.markdown("""

   <style>
    /* Force Light Pink Background */
    [data-testid="stAppViewContainer"] {
        background-color: #ffccdd !important;
    }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #2c3e50 !important;
        color: white !important;
    }
    [data-testid="stSidebar"] * {
        color: white !important;
    }

    /* Header */
    .header {
        color: #2c3e50; 
        padding: 20px; 
        text-align: center;
    }

    /* Book Card */
    .book-card {
        padding: 20px;
        margin: 15px 0;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        background: white;
        transition: transform 0.2s;
    }
    .book-card:hover {
        transform: translateY(-2px);
    }

    /* Statistics Text Fix */
    .stats {
        font-size: 1.2em; 
        color: white !important;  /* Changed from green to white */
        padding: 10px;
    }

    /* Buttons */
    .stButton>button {
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

def add_book_form():
    with st.form("add_book_form", clear_on_submit=True):
        st.subheader("📖 Add New Book")
        title = st.text_input("Book Title")
        author = st.text_input("Author")
        year = st.number_input("Publication Year", 1800, datetime.now().year)
        genre = st.selectbox("Genre", ["Fiction", "Non-Fiction", "Science", "History", "Biography", "Poetry", "Other"])
        read_status = st.radio("Read Status", ("Yes", "No"))

        if st.form_submit_button("Add Book ➕"):
            if title and author:
                new_book = {
                    "title": title,
                    "author": author,
                    "year": int(year),
                    "genre": genre,
                    "read": read_status == "Yes"
                }
                library = load_library()
                library.append(new_book)
                save_library(library)
                st.success("Book added successfully! 🎉")
            else:
                st.error("Please fill in all required fields!")

def remove_book_section():
    st.subheader("🗑️ Remove Book")
    library = load_library()
    if library:
        books = [f"{book['title']} by {book['author']}" for book in library]
        selected = st.selectbox("Select book to remove", books)
        if st.button("❌ Delete Book"):
            index = books.index(selected)
            del library[index]
            save_library(library)
            st.success("Book deleted successfully! 🔥")
            if len(library) == 0:
                save_library(DEFAULT_BOOKS)
                st.info("📚 Default books restored!")  
    else:
        st.info("Your library is empty 📭")

def search_books():
    st.subheader("🔍 Search Books")
    library = load_library()
    search_type = st.radio("Search By", ("Title", "Author"))
    query = st.text_input("Enter search term")

    if query:
        results = []
        if search_type == "Title":
            results = [book for book in library if query.lower() in book['title'].lower()]
        else:
            results = [book for book in library if query.lower() in book['author'].lower()]

        if results:
            st.subheader(f"📚 Found {len(results)} Books")
            for book in results:
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <h4>{book['title']}</h4>
                        <p>✍️ Author: {book['author']}</p>
                        <p>📅 Year: {book['year']} | 🏷️ Genre: {book['genre']}</p>
                        <p>{"✅ Read" if book['read'] else "❌ Unread"}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.warning("No matching books found!")

def show_statistics():
    st.subheader("📊 Library Statistics")
    library = load_library()
    total_books = len(library)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"<div class='stats'>📚 Total Books: {total_books}</div>", unsafe_allow_html=True)

    if total_books > 0:
        read_books = sum(book['read'] for book in library)
        read_percentage = (read_books / total_books) * 100
        with col2:
            st.markdown(f"<div class='stats'>📖 Read: {read_percentage:.1f}%</div>", unsafe_allow_html=True)

        genres = [book['genre'] for book in library]
        genre_count = {genre: genres.count(genre) for genre in set(genres)}
        st.write("---")
        st.subheader("📊 Genre Distribution")
        st.bar_chart(genre_count)

        st.write("---")
        st.subheader("📅 Publication Timeline")
        years = [book['year'] for book in library]
        if years:
            timeline_data = {'Year': years}
            st.line_chart(timeline_data)
    else:
        st.info("Your library is empty!")

# Main App
def main():
    st.title("📚 Personal Library Manager")

    
    menu = st.sidebar.radio("📖 Menu", ["🏠 Home", "➕ Add Book", "🗑️ Remove Book", "🔍 Search", "📊 Statistics"])

    if menu == "🏠 Home":
        st.header("Your Library 📚")
        library = load_library()
        if library:
            for book in library:
                with st.container():
                    st.markdown(f"""
                    <div class="book-card">
                        <h4>{book['title']}</h4>
                        <p>✍️ Author: {book['author']}</p>
                        <p>📅 Year: {book['year']} | 🏷️ Genre: {book['genre']}</p>
                        <p>{"✅ Read" if book['read'] else "❌ Unread"}</p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("📭 Your library is empty! Start by adding books.")

    elif menu == "➕ Add Book":
        add_book_form()

    elif menu == "🗑️ Remove Book":
        remove_book_section()

    elif menu == "🔍 Search":
        search_books()

    elif menu == "📊 Statistics":
        show_statistics()

if __name__ == "__main__":
    main()




