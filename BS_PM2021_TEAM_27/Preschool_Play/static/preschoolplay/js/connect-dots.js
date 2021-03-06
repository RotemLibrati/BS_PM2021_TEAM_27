function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === name + "=") {
                cookieValue = decodeURIComponent(
                    cookie.substring(name.length + 1)
                );
                break;
            }
        }
    }
    return cookieValue;
}

function mousePressed() {
    options.chosenShape.clickDot();
    options.chosenShape.clickAnswer();
}
const options = {
    canvasWidth: 600,
    canvasHeight: 500,
    generalSizeMultiplier: 1,
    difficultyLevel:
        typeof givenDifficulty !== "undefined" ? givenDifficulty : 1,
    difficultyAdder: 0,
    initDifficuly: function initDifficuly() {
        if (this.difficultyLevel == 2) {
            this.difficultyAdder = 1 + Math.floor(Math.random() * 4);
        }
        if (this.difficultyLevel == 3) {
            this.difficultyAdder = 8 + Math.floor(Math.random() * 4);
        }
    },
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
            amount: 5 * options.difficultyLevel,
            comment: "comment placeholder",
        };
        let csrftoken = getCookie("csrftoken");
        let response = fetch(
            "http://127.0.0.1:8000/preschoolplay/send-game-info",
            {
                method: "POST",
                body: JSON.stringify(data),
                headers: { "X-CSRFToken": csrftoken },
            }
        );
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
                    this.MEIndex = Math.floor(
                        Math.random() * this.mistakeEncouragements.length
                    );
                }
            }
        }
    },
    get randomShape() {
        return this.shapes[Math.floor(Math.random() * this.shapes.length)];
    },
    drawVictoryText: function drawVictoryText() {
        push();
        fill(20, 230, 20);
        stroke(5);
        textSize(100);
        text(
            this.positiveFeedback[this.PFIndex],
            this.canvasWidth / 2 - textWidth(this.positiveFeedback[this.PFIndex]) / 2,
            this.canvasHeight / 3
        );
        pop();
    },
    mistakeEncouragements: ["????????", "???????????? ??????", "????????", "???? ??????????"],
    MEIndex: 0,
    positiveFeedback: ["???????? ????", "??????????", "??????????", "???? ??????????"],
    PFIndex: 0,
    shuffleWrongAnswers: function shuffleWrongAnswers() {
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
    },
    drawDots: function drawDots(j = 0) {
        if (this.isSolved) {
            return;
        }
        j = Math.floor(j % this.dots.length);
        this.startIndex = j;
        push();
        for (let i = 0; i < this.dots.length; i++) {
            if (this.dots[j].isClicked) {
                push();
                let fromDot =
                    this.dots[(j + this.dots.length - 1) % this.dots.length];
                fill(0);
                stroke(0);
                strokeWeight(9);
                line(fromDot.x, fromDot.y, this.dots[j].x, this.dots[j].y);
                pop();
            }
            j = (j + 1) % this.dots.length;
        }
        j = Math.floor(j % this.dots.length);
        for (let i = 0; i < this.dots.length; i++) {
            if (this.dots[j].isClicked) {
                fill(50, 255, 50);
            } else {
                const timeNow = new Date();
                if (timeNow - this.dots[j].lastTimePressed < 3000) {
                    push();
                    stroke(230, 50, 50);
                    textSize(50);
                    text(
                        this.mistakeEncouragements[this.MEIndex],
                        this.canvasWidth / 2 -
                            textWidth(
                                this.mistakeEncouragements[this.MEIndex]
                            ) /
                                2,
                        (this.canvasHeight * 7) / 8
                    );
                    pop();
                }
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
            text(
                i + this.difficultyAdder,
                this.dots[j].x - 5,
                this.dots[j].y + 5
            );
            j = (j + 1) % this.dots.length;
        }
        pop();
        this.isSolved = true;
        for (let i = 0; i < this.dots.length; i++) {
            if (!this.dots[i].isClicked) {
                this.isSolved = false;
            }
        }
    },
    clickAnswer: function clickAnswer() {
        if (this.isSolved) {
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
        }
    },
};
const house = Object.create(options);
options.shapes.push(house);
const car = Object.create(options);
options.shapes.push(car);
const door = Object.create(options);
options.shapes.push(door);
door.initShape = function initShape(){
    this.specificSizeMultiplier = 1;
    this.dots = [
        {//left top
            x: this.canvasWidth / 3,
            y: (this.canvasHeight )/ 5 ,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            //left center
            x: this.canvasWidth /3,
            y: (this.canvasHeight *2 )/ 4 ,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {//left down
            x: this.canvasWidth  /3,
            y: (this.canvasHeight *4)/5 ,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {//right down
            x: this.canvasWidth *2 /3,
            y: (this.canvasHeight *4)/5 ,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {//right center
            x: this.canvasWidth *2 /3,
            y: (this.canvasHeight *2 )/ 4 ,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            // top right
            x: this.canvasWidth *2 /3,
            y: (this.canvasHeight )/ 5 ,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
    ];
    this.randStartPoint = Math.floor(Math.random() * this.dots.length);
    this.clickIndex = 0;
    this.dotRadius = 40;
    this.isSolved = false;
    this.isComplete = false;
    this.rightAnswer = "??????";
    this.rightAnswerIndex = 0;
    this.wrongAnswers = ["??????", "????????", "????????", "??????????"];
    this.shuffleWrongAnswers = function shuffleWrongAnswers() {
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
    this.drawDots = function drawDots(j = 0) {
        if (this.isSolved) {
            return;
        }
        j = Math.floor(j % this.dots.length);
        this.startIndex = j;
        push();
        for (let i = 0; i < this.dots.length; i++) {
            if (this.dots[j].isClicked) {
                push();
                let fromDot =
                    this.dots[(j + this.dots.length - 1) % this.dots.length];
                fill(0);
                stroke(0);
                strokeWeight(9);
                line(fromDot.x, fromDot.y, this.dots[j].x, this.dots[j].y);
                pop();
            }
            j = (j + 1) % this.dots.length;
        }
        j = Math.floor(j % this.dots.length);
        for (let i = 0; i < this.dots.length; i++) {
            if (this.dots[j].isClicked) {
                fill(50, 255, 50);
            } else {
                const timeNow = new Date();
                if (timeNow - this.dots[j].lastTimePressed < 3000) {
                    push();
                    stroke(230, 50, 50);
                    textSize(50);
                    text(
                        this.mistakeEncouragements[this.MEIndex],
                        this.canvasWidth / 2 -
                            textWidth(
                                this.mistakeEncouragements[this.MEIndex]
                            ) /
                                2,
                        (this.canvasHeight * 7) / 8
                    );
                    pop();
                }
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
            text(
                i + this.difficultyAdder,
                this.dots[j].x - 5,
                this.dots[j].y + 5
            );
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
    this.drawShape = function drawShape() {
        if (!this.isSolved) {
            return;
        }
        const multiplier =
            this.generalSizeMultiplier * this.specificSizeMultiplier;
        const canvasWidthCenter = this.canvasWidth / 2;
        const cnavasHeightCenter = this.canvasHeight / 2;
        const shapeHeightmodifier = -80;
        push();
        fill(150, 75, 0);
        rectMode(CENTER);
        rect(
             canvasWidthCenter,
            (cnavasHeightCenter ) ,
            (this.canvasWidth ) / 3,
            (this.canvasHeight *4)/6
        );
        push();
        rectMode(CENTER);
        rect(
            (canvasWidthCenter*100)/101,
            (cnavasHeightCenter *7)/10 ,
            (this.canvasWidth/4),
            (this.canvasHeight*2)/8
        );
        push();
        fill(0);
        rectMode(CENTER);
        circle(
            (this.canvasWidth * 4) / 10,
            (this.canvasHeight * 5) / 7 + shapeHeightmodifier,
            20
        );
        pop();
        pop();
        pop();
    };

    this.drawQuestion = function drawQuestion() {
        if (!this.isSolved) {
            return;
        }
        push();
        rectMode(CENTER);
        fill(50, 50, 255);
        textSize(20);
        text(
            "????? ?????????? ????????????",
            this.canvasWidth / 2 - textWidth("????? ?????????? ????????????") / 2,
            this.canvasHeight * 0.9
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
}
car.initShape = function initShape() {
    this.specificSizeMultiplier = 1;
    this.dots = [
        {
            x: this.canvasWidth / 12,
            y: (this.canvasHeight * 3) / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: this.canvasWidth / 12,
            y: this.canvasHeight / 2,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: this.canvasWidth / 5,
            y: this.canvasHeight / 2,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 4) / 12,
            y: this.canvasHeight / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 7) / 12,
            y: this.canvasHeight / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 2) / 3,
            y: this.canvasHeight / 2,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 5) / 6,
            y: this.canvasHeight / 2,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 5) / 6,
            y: (this.canvasHeight * 3) / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
    ];
    this.randStartPoint = Math.floor(Math.random() * this.dots.length);
    this.clickIndex = 0;
    this.dotRadius = 40;
    this.isSolved = false;
    this.isComplete = false;
    this.rightAnswer = "????????????";
    this.rightAnswerIndex = 0;
    this.wrongAnswers = ["????", "??????", "??????", "????????"];
    this.drawShape = function drawShape() {
        if (!this.isSolved) {
            return;
        }
        const multiplier =
            this.generalSizeMultiplier * this.specificSizeMultiplier;
        const canvasWidthCenter = this.canvasWidth / 2;
        const cnavasHeightCenter = this.canvasHeight / 2;
        const shapeHeightmodifier = -80;
        push();
        fill(0, 0, 230);
        rectMode(CENTER);
        rect(
            canvasWidthCenter,
            cnavasHeightCenter + shapeHeightmodifier,
            this.canvasWidth / 3,
            this.canvasHeight / 4
        );
        rect(
            canvasWidthCenter,
            (cnavasHeightCenter * 4) / 3 + shapeHeightmodifier,
            (this.canvasWidth * 5) / 6,
            this.canvasHeight / 4
        );
        triangle(
            (this.canvasWidth * 2) / 6,
            (this.canvasHeight * 3) / 8 + shapeHeightmodifier,
            (this.canvasWidth * 2) / 6,
            (this.canvasHeight * 13) / 24 + shapeHeightmodifier,
            (this.canvasWidth * 2) / 9,
            (this.canvasHeight * 13) / 24 + shapeHeightmodifier
        );
        triangle(
            (this.canvasWidth * 4) / 6,
            (this.canvasHeight * 3) / 8 + shapeHeightmodifier,
            (this.canvasWidth * 4) / 6,
            (this.canvasHeight * 13) / 24 + shapeHeightmodifier,
            (this.canvasWidth * 7) / 9,
            (this.canvasHeight * 13) / 24 + shapeHeightmodifier
        );
        push();
        fill(0);
        circle(
            this.canvasWidth / 3,
            (this.canvasHeight * 4) / 5 + shapeHeightmodifier,
            80
        );
        circle(
            (this.canvasWidth * 2) / 3,
            (this.canvasHeight * 4) / 5 + shapeHeightmodifier,
            80
        );
        pop();
        pop();
    };
    this.drawQuestion = function drawQuestion() {
        if (!this.isSolved) {
            return;
        }
        push();
        rectMode(CENTER);
        fill(50, 50, 255);
        textSize(20);
        text(
            "????? ?????????? ????????????",
            this.canvasWidth / 2 - textWidth("????? ?????????? ????????????") / 2,
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
};
house.initShape = function initShape() {
    this.specificSizeMultiplier = 1;
    this.dots = [
        {
            x: this.canvasWidth / 4,
            y: (this.canvasHeight * 3) / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: this.canvasWidth / 4,
            y: this.canvasHeight / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: this.canvasWidth / 2,
            y: this.canvasHeight / 8,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 3) / 4,
            y: this.canvasHeight / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
        {
            x: (this.canvasWidth * 3) / 4,
            y: (this.canvasHeight * 3) / 4,
            isClicked: false,
            lastTimePressed: new Date() + 1,
        },
    ];
    this.randStartPoint = Math.floor(Math.random() * this.dots.length);
    this.clickIndex = 0;
    this.dotRadius = 40;
    this.isSolved = false;
    this.isComplete = false;
    this.rightAnswer = "??????";
    this.rightAnswerIndex = 0;
    this.wrongAnswers = ["????", "??????", "????????????", "????????"];
    this.drawShape = function drawShape() {
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
    this.drawQuestion = function drawQuestion() {
        if (!this.isSolved) {
            return;
        }
        push();
        rectMode(CENTER);
        fill(50, 50, 255);
        textSize(20);
        text(
            "????? ?????????? ????????????",
            this.canvasWidth / 2 - textWidth("????? ?????????? ????????????") / 2,
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
};

function setup() {
    createCanvas(options.canvasWidth, options.canvasHeight);
    options.chosenShape = options.randomShape;
    options.initDifficuly();
    options.chosenShape.initShape();
    options.chosenShape.shuffleWrongAnswers();
    options.chosenShape.rightAnswerIndex = Math.floor(Math.random() * 3);
    options.PFIndex = Math.floor(Math.random()*options.positiveFeedback.length);
}
function draw() {
    background(220);
    options.chosenShape.drawDots(options.chosenShape.randStartPoint);
    options.chosenShape.drawShape();
    options.chosenShape.drawQuestion();
    if (options.chosenShape.isComplete) {
        options.drawVictoryText();
    }
}
