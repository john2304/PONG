// Global variables for game state
let stop;
let canvas, canvas_context;
let p1y, p2y, pt, ph, bx, by, bd, xv, yv;
let score1, score2;
let winPoint;
let reboundSound;
let ais;
let names;

function setupGameVariables() {
    // Initialize game variables
    var stop;
    var wait = 1000;
    var keep_going = true;

    //paddle y, thickness, height
    p1y = p2y = 40;
    pt = 10;
    ph = 100;
    //ball x, y, dimension
    bx = by = 50;
    bd = 6;

    //track score
    score1 = score2 = 0;

    // score to play to
    win_point = {{win_point}}

    // initial velocity of ball
    xv = yv = 10;

    //audio
    var rebound_sound = new Audio('/static/sounds/bounce.mp3');

    // speed ai moves paddle
    var ais = {{ai_speed}}


    // cast python list to json
    var names = {{names|tojson}}

function setupGame() {
    // Code to initialize the game (canvas setup, event listeners, etc.)
    // This function prepares the game but doesn't start it
    // main game
    window.onload = function () {
        canvas = document.getElementById("canvas");
        canvas_context = canvas.getContext("2d");

        // frame rate for game
        stop = setInterval(update, 1000 / 30);

        //user controls
        canvas.addEventListener("mousemove", function (e) {
            // keep center of paddle 1 at location of users mouse
            p1y = e.clientY - ph;
        });

    }
}

function startGame() {
    // Code to start your Pong game
    // This function initiates the game logic and loop
    setupGameVariables();
    setupGame(); // Initialize the game

    // Start game loop
    stop = setInterval(update, 1000 / 30);
}

function reset() {
    // center ball
    bx = canvas.width / 2;
    by = canvas.height / 2;

    // reverse x velocity
    xv = -xv;

    // start ball moving
    yv = 3;
}

function update() {
    if (score1 == win_point || score2 == win_point) {
        clearInterval(stop);
        calculate_score()
    }

    // move ball, add velocity to coordinate of ball
    bx += xv;
    by += yv;

    // bounce ball at edges of screen
    // if ball is at bottom of screen trying to move down
    if (by < 0 && yv < 0) {
        // reverse y velocity
        yv = -yv
    }
    // if ball is at top of screen trying to move up
    if (by > canvas.height && yv > 0) {
        // reverse y velocity
        yv = -yv
    }

    // if ball is at left side of screen
    if (bx < 0) {
        // if ball is above bottom of paddle and below top of paddle, bounce it
        if (by > p1y && by < p1y + ph) {

            //play rebound sound
            if (play_fx) {
                rebound_sound.play();
            }

            // reverse x velocity
            xv = -xv;
            // reduce y velocity depending on where on the paddle the ball hits
            dy = by - (p1y + ph / 2);
            yv = dy * 0.3;
        }
        // paddle1 missed ball
        else {
            // award player 2 one point, reset game
            score2 = score2 + 1;
            reset();
        }
    }

    // if ball is at right of screen
    if (bx > canvas.width) {
        // if ball is above bottom of paddle and below top of paddle, bounce it
        if (by > p2y && by < p2y + ph) {

            //play rebound sound
            if (play_fx) {
                rebound_sound.play();
            }

            // reverse x velocity
            xv = -xv;
            // reduce y velocity depending on where on the paddle the ball hits
            dy = by - (p2y + ph / 2);
            yv = dy * 0.3;
        }
        // paddle1 missed ball
        else {
            // award player 1 one point, reset game
            score1 = score1 + 1;
            reset();
        }
    }

    // player 2 is AI, will try to keep center of paddle 2 in line with ball y coordinate
    if (p2y + ph / 2 < by) {
        requestAnimationFrame(function () {
            p2y += ais;
        });
    } else {
        p2y -= ais;
    }


    canvas_context.fillStyle = "black";
    canvas_context.fillRect(0, 0, canvas.width, canvas.height);


    canvas_context.fillStyle = "white";
    // draw paddles, that's a paddlin
    canvas_context.fillRect(0, p1y, pt, ph);
    canvas_context.fillRect(canvas.width - pt, p2y, pt, ph);

    // ball
    canvas_context.fillRect(bx - bd / 2, by - bd / 2, bd, bd);

    //score1 on left of screen, score2 on right
    canvas_context.fillText(score1, 100, 100);
    canvas_context.fillText(score2, canvas.width - 100, 100);

}

// get score and add value to hidden form
var calculate_score = function () {
    // console.log("submit " + score1 + ", " + score2);

    // show hidden form
    document.getElementById("form-hidden").style.display = "block";

    // calculate score, may be redundant if function is just used to toggle view, but isn't expensive
    document.getElementById("score").value = score1 - score2;

    document.getElementById("show_score").innerHTML = "Score: " + (score1 - score2);
};

var play_again = function () {
    //hide submit form
    document.getElementById("form-hidden").style.display = "none";

    //reset scores
    score1 = score2 = 0;
    // reset ball and paddles
    reset()

    // start game loop
    keep_going = true;
    stop = setInterval(update, 1000 / 30);
}

$(document).ready(function () {
    // Event listener for the "Start Game" button
    $('start-button').click(function () {
        startGame(); // Call the startGame function when the button is clicked
        console.log('Button Clicked!'); // Add a console log statement for testing
    })
}


// continuously validate form input, show user that a unique name must be chosen
$("#user_name").change(function () {
    if (names.includes($("#user_name").val())) {
        // stop user from submitting form with invalid name
        $("#errors").text("Sorry, this name is taken").css({"color": "red"});
        $('#submitButton').attr("disabled", true);
    } else {
        // allow user to submit form again
        $("#errors").text("This name is free!").css({"color": "green"});
        $('#submitButton').attr("disabled", false);
    }
});


// Event listener for the "Start Game" button using pure JavaScript
document.addEventListener('DOMContentLoaded', function() {
    let startButton = document.getElementById('start-game-button');
    startButton.addEventListener('click', function() {
        startGame(); // Call the startGame function when the button is clicked
        console.log('Button Clicked!'); // For testing
    });
});
