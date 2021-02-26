<!DOCTYPE html>
<html>
<head>
    <title>Authorization Failure</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">

    <link rel="icon" type="image/png" sizes="32x32" href="/static/favicon.png">
    <link rel="icon" type="image/png" sizes="16x16" href="/static/favicon.png">

    <style>
        * {
            margin: 0;
            padding: 0;
            color: white;
            font-family: "Montserrat", sans-serif;
            box-sizing: border-box;
        }
        body {
            background-color: #800080;
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
            padding: 50px;
        }
        h1, p {
            margin-bottom: 10px;
        }
        span {
            background: #333333;
            padding: 2px 5px;
            border: 1px solid gray;
            border-radius: 10px;
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
        <img src="/static/wichacks.jpg" alt="Authbot found a problem.">
        <div>
            <h1>Authorization Failed!</h1>
            <p>{{ reason }}</p>
            <p>For assistance, send us a message in <span>#check-in-desk</span></p>
        </div>
    </main>
</body>
</html>
