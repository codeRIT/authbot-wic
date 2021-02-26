<!DOCTYPE html>
<html>
<head>
    <title>Authorization Success!</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap" rel="stylesheet">

    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon-32x32.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon-16x16.png">

    <style>
        * {
            margin: 0;
            padding: 0;
            color: white;
            font-family: "Poppins", sans-serif;
            box-sizing: border-box;
        }
        body {
            background-color: #2A407D;
        }
        main {
            min-height: 100vh;
            padding: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        img {
            width: 300px;
            border-radius: 20px;
        }
        div {
            padding: 0 0 0 50px;
        }
        h1, p {
            margin-bottom: 10px;
        }
        #button {
            background-color: #F1656E;
            text-decoration: none;
            user-select: none;
            padding: 10px 20px;
            cursor: pointer;
            border-radius: 50px;
            transition: 0.2s all;
            display: inline-block;
        }
        #button:hover {
            filter: brightness(110%);
        }
        #button:active {
            transform: translateY(4px);
        }
        @media only screen and (max-width: 800px) {
            main {
                flex-direction: column;
            }
            img {
                width: auto;
                max-width: 80%;
            }
            div {
                padding: 50px 0 0 0;
                text-align: center;
            }
        }
    </style>
</head>
<body>
    <main>
        <img src="/static/authbotSuccess.png" alt="Authbot welcomes you!">
        <div>
            <h1>Authorization Success!</h1>
            <p>Your Discord and BrickHack accounts are successfully linked!</p>
            <p>Head back to Discord to follow up with AuthBot.</p>
        </div>
    </main>
</body>
</html>
