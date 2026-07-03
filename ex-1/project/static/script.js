async function search() {

    let array = document
        .getElementById("array")
        .value
        .split(",")
        .map(Number);

    let key = Number(document.getElementById("key").value);

    const response = await fetch("/interpolate", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            array: array,
            key: key

        })

    });

    const data = await response.json();

    const result = document.getElementById("result");

    if (data.success) {

        result.style.background = "#d4edda";
        result.style.color = "#155724";

        result.innerHTML =

            "<p><b>Sorted Array:</b> "
            + data.array.join(", ")
            + "</p><br>"

            + data.message;

    }

    else {

        result.style.background = "#f8d7da";
        result.style.color = "#721c24";

        result.innerHTML =

            "<p><b>Sorted Array:</b> "
            + data.array.join(", ")
            + "</p><br>"

            + data.message;
    }

}