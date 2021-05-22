function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
}

function mousePressed() {
    house.clickDot();
    house.clickAnswer();
}
const options = {
    canvasWidth: 600,
    canvasHeight: 500,
    generalSizeMultiplier: 1,
    difficultyLevel: 1,
    mistakeCounter: 0,
    dataSent: false,
    sendData: function sendData() {
        if (this.dataSent) {
            return;
        }
        let data = {
            difficultyLevel: this.difficultyLevel,
            mistakeCounter: this.mistakeCounter,
            child: childName,
            amount: 5,
            comment: 'comment placeholder',
        };
        let csrftoken = getCookie("csrftoken");
        let response = fetch("http://127.0.0.1:8000/preschoolplay/send-game-info", {
            method: "POST",
            body: JSON.stringify(data),
            headers: { "X-CSRFToken": csrftoken },
        });
        this.dataSent = true;
    },
    shapes: [],
    chosenShape: null,
    clickDot: function clickDot() {
        for (let i = 0; i < this.dots.length; i++) {
            if (
                dist(this.dots[i].x, this.dots[i].y, mouseX, mouseY) <=
                this.dotRadius
            ) {
                this.dots[i].lastTimePressed = new Date();
                if (
                    i ==
                    (this.startIndex + this.clickIndex) % this.dots.length
                ) {
                    this.dots[i].isClicked = true;
                    this.clickIndex++;
                } else {
                    this.mistakeCounter++;
                }
            }
        }
    },
    get randomShape() {
        return this.shapes[Math.floor(Math.random() * this.shapes.length)];
    },
};
const house = Object.create(options);
options.shapes.push(house);
house.initShape = function initShape() {
    house.specificSizeMultiplier = 1;
    house.dots = [
        {
            x: house.canvasWidth / 4,
            y: (house.canvasHeight * 3) / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: house.canvasWidth / 4,
            y: house.canvasHeight / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: house.canvasWidth / 2,
            y: house.canvasHeight / 8,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (house.canvasWidth * 3) / 4,
            y: house.canvasHeight / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (house.canvasWidth * 3) / 4,
            y: (house.canvasHeight * 3) / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
    ];
    house.randStartPoint = Math.floor(Math.random() * house.dots.length);
    house.clickIndex = 0;
    house.dotRadius = 40;
    house.isSolved = false;
    house.isComplete = false;
    house.rightAnswer = "בית";
    house.rightAnswerIndex = 0;
    house.wrongAnswers = ["הר", "חיה", "מכונית", "מיטה"];
    house.shuffleWrongAnswers = function shuffleWrongAnswers() {
        function shuffleArr(array) {
            var currentIndex = array.length,
                temporaryValue,
                randomIndex;
            while (0 !== currentIndex) {
                randomIndex = Math.floor(Math.random() * currentIndex);
                currentIndex -= 1;
                temporaryValue = array[currentIndex];
                array[currentIndex] = array[randomIndex];
                array[randomIndex] = temporaryValue;
            }
            return array;
        }
        this.wrongAnswers = shuffleArr(this.wrongAnswers);
    };
    house.drawDots = function drawDots(j = 0) {
        if (this.isSolved) {
            return;
        }
        j = Math.floor(j % this.dots.length);
        this.startIndex = j;
        push();
        for (let i = 0; i < this.dots.length; i++) {
            if (this.dots[j].isClicked) {
                fill(50, 255, 50);
            } else {
                const timeNow = new Date();
                if (timeNow - this.dots[j].lastTimePressed < 1500) {
                    fill(230, 50, 50);
                } else {
                    fill(230);
                }
            }
            ellipse(
                this.dots[j].x,
                this.dots[j].y,
                this.dotRadius,
                this.dotRadius
            );
            fill(0);
            textSize(15);
            text(i, this.dots[j].x - 5, this.dots[j].y + 5);
            j = (j + 1) % this.dots.length;
        }
        pop();
        this.isSolved = true;
        for (let i = 0; i < this.dots.length; i++) {
            if (!this.dots[i].isClicked) {
                this.isSolved = false;
            }
        }
    };
    house.drawShape = function drawShape() {
        if (!this.isSolved) {
            return;
        }
        const multiplier =
            this.generalSizeMultiplier * this.specificSizeMultiplier;
        const canvasWidthCenter = this.canvasWidth / 2;
        const cnavasHeightCenter = this.canvasHeight / 2;
        push();
        fill(230, 0, 0);
        rectMode(CENTER);
        rect(
            canvasWidthCenter,
            cnavasHeightCenter,
            canvasWidthCenter,
            cnavasHeightCenter
        );
        const rectTopLeftX = this.canvasWidth / 4;
        const rectTopRightX = (this.canvasWidth * 3) / 4;
        const rectTopBorderY = this.canvasHeight / 4;
        const roofY = this.canvasHeight / 8;
        triangle(
            rectTopLeftX - 25,
            rectTopBorderY,
            rectTopRightX + 25,
            rectTopBorderY,
            canvasWidthCenter,
            roofY
        );
        noFill();
        strokeWeight(11);
        stroke(150, 0, 0);
        rect(
            rectTopLeftX + this.canvasWidth / 10,
            rectTopBorderY + this.canvasWidth / 10,
            this.canvasWidth / 20,
            this.canvasWidth / 20
        );
        rect(
            canvasWidthCenter,
            (this.canvasHeight * 3) / 4 - this.canvasHeight / 10 - 5,
            this.canvasWidth / 15,
            this.canvasHeight / 5
        );
        pop();
    };
    house.drawQuestion = function drawQuestion() {
        if (!this.isSolved) {
            return;
        }
        push();
        rectMode(CENTER);
        fill(50, 50, 255);
        textSize(20);
        text(
            "?מה רואים בתמונה",
            this.canvasWidth / 2 - textWidth("?מה רואים בתמונה") / 2,
            this.canvasHeight * 0.85
        );
        if (this.isComplete && this.rightAnswerIndex == 0) {
            fill(0, 255, 0);
        } else {
            fill(50, 50, 255);
        }
        rect(
            this.canvasWidth / 3,
            this.canvasHeight * 0.95,
            this.canvasWidth / 9,
            this.canvasHeight / 12
        );
        if (this.isComplete && this.rightAnswerIndex == 1) {
            fill(0, 255, 0);
        } else {
            fill(50, 50, 255);
        }
        rect(
            this.canvasWidth / 2,
            this.canvasHeight * 0.95,
            this.canvasWidth / 9,
            this.canvasHeight / 12
        );
        if (this.isComplete && this.rightAnswerIndex == 2) {
            fill(0, 255, 0);
        } else {
            fill(50, 50, 255);
        }
        rect(
            (this.canvasWidth * 2) / 3,
            this.canvasHeight * 0.95,
            this.canvasWidth / 9,
            this.canvasHeight / 12
        );
        fill(0);
        let i = 0;
        let txt = "";
        if (i == this.rightAnswerIndex) {
            txt = this.rightAnswer;
        } else {
            txt = this.wrongAnswers[i];
        }
        i++;
        text(
            txt,
            this.canvasWidth / 3 - textWidth(txt) / 2,
            this.canvasHeight * 0.95
        );
        if (i == this.rightAnswerIndex) {
            txt = this.rightAnswer;
        } else {
            txt = this.wrongAnswers[i];
        }
        i++;
        text(
            txt,
            this.canvasWidth / 2 - textWidth(txt) / 2,
            this.canvasHeight * 0.95
        );
        if (i == this.rightAnswerIndex) {
            txt = this.rightAnswer;
        } else {
            txt = this.wrongAnswers[i];
        }
        text(
            txt,
            (this.canvasWidth * 2) / 3 - textWidth(txt) / 2,
            this.canvasHeight * 0.95
        );
        pop();
    };
    house.clickAnswer = function clickAnswer() {
        if (
            this.rightAnswerIndex == 0 &&
            this.canvasWidth / 3 - this.canvasWidth / 18 <= mouseX &&
            mouseX <= this.canvasWidth / 3 + this.canvasWidth / 18 &&
            this.canvasHeight * 0.95 - this.canvasHeight / 24 <= mouseY &&
            mouseY <= this.canvasHeight * 0.95 + this.canvasHeight / 24
        ) {
            this.isComplete = true;
            this.sendData();
        } else if (
            this.rightAnswerIndex == 1 &&
            this.canvasWidth / 2 - this.canvasWidth / 18 <= mouseX &&
            mouseX <= this.canvasWidth / 2 + this.canvasWidth / 18 &&
            this.canvasHeight * 0.95 - this.canvasHeight / 24 <= mouseY &&
            mouseY <= this.canvasHeight * 0.95 + this.canvasHeight / 24
        ) {
            this.isComplete = true;
            this.sendData();
        } else if (
            this.rightAnswerIndex == 2 &&
            (this.canvasWidth * 2) / 3 - this.canvasWidth / 18 <= mouseX &&
            mouseX <= (this.canvasWidth * 2) / 3 + this.canvasWidth / 18 &&
            this.canvasHeight * 0.95 - this.canvasHeight / 24 <= mouseY &&
            mouseY <= this.canvasHeight * 0.95 + this.canvasHeight / 24
        ) {
            this.isComplete = true;
            this.sendData();
        }
    };
};

function setup() {
    createCanvas(options.canvasWidth, options.canvasHeight);
    options.chosenShape = options.randomShape;
    options.chosenShape.initShape();
    options.chosenShape.shuffleWrongAnswers();
    options.chosenShape.rightAnswerIndex = Math.floor(Math.random() * 3);
}
function draw() {
    background(220);
    options.chosenShape.drawDots(options.chosenShape.randStartPoint);
    options.chosenShape.drawShape();
    options.chosenShape.drawQuestion();
}
