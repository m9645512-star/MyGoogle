from flask import Flask, jsonify, request
from flask_cors import CORS
import sqlite3
import os


# ==========================================
# MyGoogle Backend
# Render Ready
# ==========================================

app = Flask(__name__)

CORS(app)


# ==========================================
# Database Path
# ==========================================

BASE_DIR = os.path.dirname(
    os.path.dirname(
        os.path.abspath(__file__)
    )
)

DATABASE_FOLDER = os.path.join(
    BASE_DIR,
    "database"
)

DATABASE_FILE = os.path.join(
    DATABASE_FOLDER,
    "mygoogle.db"
)


os.makedirs(
    DATABASE_FOLDER,
    exist_ok=True
)



# ==========================================
# Database Connection
# ==========================================

def get_database():

    connection = sqlite3.connect(
        DATABASE_FILE
    )

    connection.row_factory = sqlite3.Row

    return connection



# ==========================================
# Create Table
# ==========================================

def create_database():

    connection = get_database()

    cursor = connection.cursor()


    cursor.execute("""
        CREATE TABLE IF NOT EXISTS websites (

            id INTEGER PRIMARY KEY AUTOINCREMENT,

            title TEXT NOT NULL,

            url TEXT NOT NULL,

            description TEXT

        )
    """)


    connection.commit()

    connection.close()



# ==========================================
# Default Data
# ==========================================

def add_default_websites():

    connection = get_database()

    cursor = connection.cursor()


    cursor.execute(
        "SELECT COUNT(*) FROM websites"
    )

    count = cursor.fetchone()[0]


    if count == 0:

        websites = [

            (
                "Minecraft",
                "https://www.minecraft.net/",
                "وب سایت رسمی Minecraft"
            ),

            (
                "YouTube",
                "https://www.youtube.com/",
                "پلتفرم ویدیویی YouTube"
            ),

            (
                "Wikipedia",
                "https://www.wikipedia.org/",
                "دانشنامه آزاد اینترنتی"
            ),

            (
                "Google",
                "https://www.google.com/",
                "موتور جستجو Google"
            ),

            (
                "GitHub",
                "https://github.com/",
                "پلتفرم برنامه نویسی"
            )

        ]


        cursor.executemany(
            """
            INSERT INTO websites
            (
                title,
                url,
                description
            )

            VALUES (?, ?, ?)
            """,

            websites
        )


        connection.commit()


    connection.close()# ==========================================
# Home API
# ==========================================

@app.route("/", methods=["GET"])
def home():

    return jsonify({
        "status": "MyGoogle Backend Running"
    })



# ==========================================
# Search API
# ==========================================

@app.route("/api/search", methods=["GET"])
def search():

    query = request.args.get(
        "q",
        ""
    ).strip()


    if query == "":

        return jsonify([])


    connection = get_database()

    cursor = connection.cursor()


    search_text = f"%{query}%"


    cursor.execute(
        """
        SELECT
            id,
            title,
            url,
            description

        FROM websites

        WHERE
            title LIKE ?
            OR url LIKE ?
            OR description LIKE ?

        ORDER BY id DESC
        """,

        (
            search_text,
            search_text,
            search_text
        )
    )


    rows = cursor.fetchall()

    connection.close()


    return jsonify([
        dict(row)
        for row in rows
    ])




# ==========================================
# Get All Websites
# ==========================================

@app.route("/api/websites", methods=["GET"])
def get_websites():

    connection = get_database()

    cursor = connection.cursor()


    cursor.execute(
        """
        SELECT *
        FROM websites
        ORDER BY id DESC
        """
    )


    websites = cursor.fetchall()

    connection.close()


    return jsonify([
        dict(site)
        for site in websites
    ])




# ==========================================
# Add Website
# ==========================================

@app.route("/api/websites", methods=["POST"])
def add_website():

    data = request.get_json()


    if not data:

        return jsonify({
            "error": "No data"
        }), 400


    title = data.get("title", "").strip()

    url = data.get("url", "").strip()

    description = data.get(
        "description",
        ""
    ).strip()



    if title == "" or url == "":

        return jsonify({
            "error":
            "Title and URL required"
        }), 400



    connection = get_database()

    cursor = connection.cursor()


    cursor.execute(
        """
        INSERT INTO websites
        (
            title,
            url,
            description
        )

        VALUES (?, ?, ?)
        """,

        (
            title,
            url,
            description
        )
    )


    connection.commit()

    new_id = cursor.lastrowid

    connection.close()


    return jsonify({

        "success": True,

        "id": new_id

    })




# ==========================================
# Delete Website
# ==========================================

@app.route(
    "/api/websites/<int:id>",
    methods=["DELETE"]
)
def delete_website(id):

    connection = get_database()

    cursor = connection.cursor()


    cursor.execute(
        """
        DELETE FROM websites
        WHERE id = ?
        """,

        (id,)
    )


    connection.commit()

    connection.close()


    return jsonify({

        "success": True

    })




# ==========================================
# Update Website
# ==========================================

@app.route(
    "/api/websites/<int:id>",
    methods=["PUT"]
)
def update_website(id):

    data = request.get_json()


    title = data.get(
        "title",
        ""
    ).strip()


    url = data.get(
        "url",
        ""
    ).strip()


    description = data.get(
        "description",
        ""
    ).strip()



    connection = get_database()

    cursor = connection.cursor()


    cursor.execute(
        """
        UPDATE websites

        SET
            title = ?,
            url = ?,
            description = ?

        WHERE id = ?

        """,

        (
            title,
            url,
            description,
            id
        )
    )


    connection.commit()

    connection.close()


    return jsonify({

        "success": True

    })




# ==========================================
# Start Server
# ==========================================

if __name__ == "__main__":

    create_database()

    add_default_websites()


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )