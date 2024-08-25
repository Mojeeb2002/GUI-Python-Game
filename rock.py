import sys
import random
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QHBoxLayout, QWidget, QFrame
from PyQt5.QtCore import Qt, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QFont, QColor, QPalette


class ModernButton(QPushButton):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setFont(QFont('Arial', 16))
        self.setFixedSize(120, 120)
        self.setStyleSheet("""
            QPushButton {
                background-color: #3498db;
                color: white;
                border: none;
                border-radius: 60px;
            }
            QPushButton:hover {
                background-color: #2980b9;
            }
            QPushButton:pressed {
                background-color: #2573a7;
            }
            QPushButton:disabled {
                background-color: #bdc3c7;
            }
        """)


class RockPaperScissorsGame(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Rock Paper Scissors Game")
        self.setGeometry(100, 100, 600, 400)
        self.setStyleSheet("background-color: #ecf0f1;")

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        self.result_label = QLabel("Choose your move!")
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.setFont(QFont('Arial', 24))
        self.result_label.setStyleSheet("color: #2c3e50; margin: 20px 0;")
        layout.addWidget(self.result_label)

        self.player_choice_label = QLabel("")
        self.player_choice_label.setAlignment(Qt.AlignCenter)
        self.player_choice_label.setFont(QFont('Arial', 16))
        self.player_choice_label.setStyleSheet("color: #27ae60; margin: 10px 0;")
        layout.addWidget(self.player_choice_label)

        self.computer_choice_label = QLabel("")
        self.computer_choice_label.setAlignment(Qt.AlignCenter)
        self.computer_choice_label.setFont(QFont('Arial', 16))
        self.computer_choice_label.setStyleSheet("color: #c0392b; margin: 10px 0;")
        layout.addWidget(self.computer_choice_label)

        button_layout = QHBoxLayout()
        self.rock_button = ModernButton("🪨")
        self.paper_button = ModernButton("📄")
        self.scissors_button = ModernButton("✂️")

        for button in [self.rock_button, self.paper_button, self.scissors_button]:
            button_layout.addWidget(button)

        layout.addLayout(button_layout)

        self.play_again_button = QPushButton("Play Again")
        self.play_again_button.setVisible(False)
        self.play_again_button.setFont(QFont('Arial', 16))
        self.play_again_button.setStyleSheet("""
            QPushButton {
                background-color: #2ecc71;
                color: white;
                border: none;
                border-radius: 20px;
                padding: 10px 20px;
            }
            QPushButton:hover {
                background-color: #27ae60;
            }
        """)
        layout.addWidget(self.play_again_button, alignment=Qt.AlignCenter)

        self.rock_button.clicked.connect(lambda: self.play_game("rock"))
        self.paper_button.clicked.connect(lambda: self.play_game("paper"))
        self.scissors_button.clicked.connect(lambda: self.play_game("scissors"))
        self.play_again_button.clicked.connect(self.reset_game)

        self.score_frame = QFrame()
        self.score_frame.setFrameShape(QFrame.StyledPanel)
        self.score_frame.setStyleSheet("background-color: white; border-radius: 10px; padding: 10px;")
        score_layout = QHBoxLayout(self.score_frame)
        self.player_score_label = QLabel("Player: 0")
        self.computer_score_label = QLabel("Computer: 0")
        score_layout.addWidget(self.player_score_label)
        score_layout.addWidget(self.computer_score_label)
        layout.addWidget(self.score_frame)

        self.player_score = 0
        self.computer_score = 0

    def computer_choice(self):
        return random.choice(["rock", "paper", "scissors"])

    def play_game(self, player_choice):
        computer_play = self.computer_choice()
        self.player_choice_label.setText(f"You chose: {self.get_emoji(player_choice)} {player_choice.capitalize()}")
        self.computer_choice_label.setText(
            f"Computer chose: {self.get_emoji(computer_play)} {computer_play.capitalize()}")

        if player_choice == computer_play:
            result = "It's a tie! 🤝"
        elif (
                (player_choice == "rock" and computer_play == "scissors") or
                (player_choice == "paper" and computer_play == "rock") or
                (player_choice == "scissors" and computer_play == "paper")
        ):
            result = "You win! 🎉"
            self.player_score += 1
        else:
            result = "You lose! 😔"
            self.computer_score += 1

        self.result_label.setText(result)
        self.update_score()
        self.animate_result()

        for button in [self.rock_button, self.paper_button, self.scissors_button]:
            button.setEnabled(False)
        self.play_again_button.setVisible(True)

    def reset_game(self):
        self.result_label.setText("Choose your move!")
        self.player_choice_label.setText("")
        self.computer_choice_label.setText("")
        for button in [self.rock_button, self.paper_button, self.scissors_button]:
            button.setEnabled(True)
        self.play_again_button.setVisible(False)

    def get_emoji(self, choice):
        emoji_map = {
            "rock": "🪨",
            "paper": "📄",
            "scissors": "✂️"
        }
        return emoji_map.get(choice, "")

    def update_score(self):
        self.player_score_label.setText(f"Player: {self.player_score}")
        self.computer_score_label.setText(f"Computer: {self.computer_score}")

    def animate_result(self):
        animation = QPropertyAnimation(self.result_label, b"pos")
        animation.setDuration(300)
        animation.setStartValue(self.result_label.pos())
        animation.setEndValue(self.result_label.pos().y() + 20)
        animation.setEasingCurve(QEasingCurve.OutBounce)
        animation.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    game = RockPaperScissorsGame()
    game.show()
    sys.exit(app.exec_())