import random
import psycopg2

class FitnessGramFeed:
    def __init__(self):
        self.db_params = {
            'dbname': 'healthclub',
            'user': 'postgres',
            'password': 'postgres',
            'host': 'localhost'
        }

    def get_db_connection(self):
        try:
            conn = psycopg2.connect(**self.db_params)
            return conn
        except Exception as e:
            print(f"An error occurred while connecting to the database: {e}")
            return None

    @staticmethod
    def display_feed():
        print("\n🏋️‍♂️🔥 Welcome to the Fitness Gram Feed! Let's get motivated! 💪")

        print("\n🚀 Random Posts:")
        posts = []
        for i in range(5):
            satisfaction_level = random.choice(["amazing", "great", "good", "challenging"])
            activities = random.choice(["HIIT workout", "yoga session", "morning run", "cycling class", "zumba"])
            emojis = random.choice(["🔥", "💥", "👊", "🌟", "😎"])
            post_content = f"Today's {activities} was {satisfaction_level}! Who's feeling pumped? {emojis}"
            likes = random.randint(0, 100)
            posts.append({"content": post_content, "likes": likes})
            print(f"\nPost {i + 1}:")
            print(f"📝 Content: {post_content}")
            print(f"❤️ Likes: {likes}")

        return posts

    def like_post(self, posts):
        choice = input("\nEnter the number of the post you want to like (1-5), or enter '0' to exit: ")
        if choice == "0":
            print("Exiting the feed. Keep crushing your goals! 💪")
            return posts
        elif choice.isdigit() and 1 <= int(choice) <= 5:
            post_index = int(choice) - 1
            posts[post_index]["likes"] += 1
            print("👍 You liked the post!")
            print(f"❤️ Likes for post {post_index + 1}: {posts[post_index]['likes']}")
            return posts
        else:
            print("❌ Invalid choice. Please enter a number between 1 and 5, or enter '0' to exit.")
            return posts

    def get_sessions(self, member_email):
        with self.get_db_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT s.SessionTime, t.Name as TrainerName
                    FROM Sessions s
                    JOIN Trainers t ON s.TrainerID = t.TrainerID
                    JOIN Members m ON s.MemberID = m.MemberID
                    WHERE m.Email = %s
                    ORDER BY s.SessionTime;
                """, (member_email,))
                sessions = cur.fetchall()
                return sessions

    def create_session_post(self, member_email):
        sessions = self.get_sessions(member_email)
        if sessions:
            print("\n🏋️‍♂️ Share Your Past Session Experience:")
            print("Here are your recent sessions:")
            for i, session in enumerate(sessions, start=1):
                print(f"{i}. {session[0]} with Trainer {session[1]}")

            choice = input("Choose the session you want to share your experience for (1-5): ")
            if choice.isdigit() and 1 <= int(choice) <= len(sessions):
                session_index = int(choice) - 1
                session = sessions[session_index]
                post_content = f"🏋️‍♂️ Session Experience:\nDate: {session[0]}\nTrainer: {session[1]}\nFeedback: "
                feedback = input("Share your experience and feedback for the session: ")
                post_content += feedback
                print("Your session experience has been posted:", post_content)
                with self.get_db_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("SELECT Name FROM Members WHERE Email = %s;", (member_email,))
                        member_name = cur.fetchone()[0]
                        print("Posting to FitnessGram Network...")
                        print(f"{member_name} shared their session experience:", post_content)
            else:
                print("Invalid choice.")
        else:
            print("No session found.")


def main():
    feed = FitnessGramFeed()
    posts = feed.display_feed()

    while True:
        print("\nOptions:")
        print("1. Like a post")
        print("2. Share your session experience")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            posts = feed.like_post(posts)
        elif choice == "2":
            member_email = input("Enter your email: ")
            feed.create_session_post(member_email)
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please enter a valid option.")


if __name__ == "__main__":
    main()
