import tkinter as tk

from PIL import Image, ImageTk

from tweet_generator import get_probable_tweet, load_tweets


class TweetWindow(tk.Tk):
    """class defining the window that the main_game will play in"""

    def __init__(self, screen_name):
        """initialiser - subclass of Tk"""
        super().__init__()
        # Get the screen name
        self.screen_name = screen_name
        self.title("@{0}".format(screen_name))
        # Generate the tweet model and identify the trigrams
        self.model = load_tweets(screen_name)
        # Get an initial tweet
        self.tweet = get_probable_tweet(self.model)
        # Create the main tweet window
        self.create_tweet_window()

    def create_tweet_window(self):
        # reset the window
        try:
            # remove previous objects
            self.tweet_frame.destroy()
            self.image.destroy()
            self.tweet_label.destroy()
            self.new_tweet.destroy()
        except Exception:
            pass

        # Get the main frame
        self.tweet_frame = tk.Frame(width=600, height=200, bd=3, relief=tk.RIDGE)
        self.tweet_frame.pack_propagate(0)
        self.tweet_frame.pack(padx=20, pady=20)

        # Get the main image to display the text on
        original = Image.open("img/{0}.png".format(self.screen_name))
        self.photo = ImageTk.PhotoImage(original)

        self.image = tk.Label(self.tweet_frame, image=self.photo, justify="center")
        self.image.place(x=0, y=0, relwidth=1, relheight=1)

        # Create the placeholder for the text
        self.tweet_label = tk.Label(
            self.tweet_frame,
            text=self.tweet,
            font=("Helvetica", 20),
            justify="left",
            wraplength=400,
        )
        self.tweet_label.pack(padx=100, pady=30)

        # Create a button to generate a new tweet
        self.new_tweet = tk.Button(self, command=self.reset)
        self.new_tweet.config(text="Get New Tweet")
        self.new_tweet.pack(padx=20, fill=tk.X)

    def reset(self):
        """Create a new tweet"""
        self.tweet = get_probable_tweet(self.model)
        self.create_tweet_window()


if __name__ == "__main__":
    TweetWindow(screen_name="realDonaldTrump").mainloop()
