/*
==========================================
   MyGoogle
   Frontend Version 2.0
==========================================
*/

const API_URL = "https://mygoogle-production.up.railway.app";


/*
==========================================
   SEARCH
==========================================
*/

async function search() {

    const input = document.getElementById("searchInput");
    const results = document.getElementById("results");
    const query = input.value.trim();

    results.innerHTML = "";

    if (query === "") {

        results.innerHTML = `
            <div class="no-results">
                لطفاً چیزی برای جستجو وارد کنید.
            </div>
        `;

        return;
    }


    results.innerHTML = `
        <div class="no-results">
            در حال جستجو...
        </div>
    `;


    try {

        const response = await fetch(
            API_URL +
            "/api/search?q=" +
            encodeURIComponent(query)
        );


        if (!response.ok) {

            throw new Error("Search failed");

        }


        const data = await response.json();


        results.innerHTML = "";


        if (data.length === 0) {

            results.innerHTML = `
                <div class="no-results">
                    نتیجه‌ای برای
                    <strong>${escapeHTML(query)}</strong>
                    پیدا نشد.
                </div>
            `;

            return;

        }



        data.forEach(item => {

            const result = document.createElement("div");

            result.className = "result";


            result.innerHTML = `

                <div class="result-url">

                    ${escapeHTML(item.url)}

                </div>


                <div
                    class="result-title"
                    onclick="openResult('${escapeAttribute(item.url)}')"
                >

                    ${escapeHTML(item.title)}

                </div>


                <div class="result-description">

                    ${escapeHTML(item.description || "")}

                </div>

            `;


            results.appendChild(result);

        });


    } catch (error) {


        console.error(error);


        results.innerHTML = `

            <div class="no-results">

                اتصال به سرور MyGoogle برقرار نشد.

                <br><br>

                مطمئن شو Backend در حال اجراست.

            </div>

        `;

    }

}



/*
==========================================
   OPEN RESULT
==========================================
*/


function openResult(url) {

    window.open(
        url,
        "_blank"
    );

}



/*
==========================================
   ENTER KEY
==========================================
*/


document

    .getElementById("searchInput")

    .addEventListener(

        "keydown",

        function(event) {

            if (event.key === "Enter") {

                search();

            }

        }

    );



/*
==========================================
   CLEAR SEARCH
==========================================
*/


function clearSearch() {

    const input =
        document.getElementById("searchInput");


    const results =
        document.getElementById("results");


    input.value = "";


    results.innerHTML = "";


    input.focus();

}



/*
==========================================
   CLEAR BUTTON
==========================================
*/


document

    .getElementById("searchInput")

    .addEventListener(

        "input",

        function() {


            const clearButton =
                document.getElementById("clearButton");


            if (this.value.length > 0) {


                clearButton.style.display = "block";


            } else {


                clearButton.style.display = "none";


            }


        }

    );/*
==========================================
   RANDOM SEARCH
==========================================
*/

async function randomSearch() {

    try {

        const response =
            await fetch(
                API_URL +
                "/api/websites"
            );


        const websites =
            await response.json();



        if (websites.length === 0) {

            return;

        }



        const randomIndex =
            Math.floor(
                Math.random() * websites.length
            );



        const randomWebsite =
            websites[randomIndex];



        const input =
            document.getElementById("searchInput");



        input.value =
            randomWebsite.title;



        search();



    } catch (error) {

        console.error(error);

    }

}



/*
==========================================
   ABOUT
==========================================
*/


function showAbout() {

    alert(

        "MyGoogle\n\n" +

        "موتور جست‌وجوی شخصی ما\n\n" +

        "نسخه 2.0\n\n" +

        "Backend: Python + Flask\n" +

        "Database: SQLite"

    );

}



/*
==========================================
   HTML SECURITY
==========================================
*/


function escapeHTML(text) {


    return String(text)

        .replace(/&/g, "&amp;")

        .replace(/</g, "&lt;")

        .replace(/>/g, "&gt;")

        .replace(/"/g, "&quot;")

        .replace(/'/g, "&#039;");


}



/*
==========================================
   ATTRIBUTE SECURITY
==========================================
*/


function escapeAttribute(text) {


    return String(text)

        .replace(/\\/g, "\\\\")

        .replace(/'/g, "\\'")

        .replace(/"/g, "&quot;");


}