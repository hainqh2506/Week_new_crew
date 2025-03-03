# Import các thư viện cần thiết
import os
from dotenv import load_dotenv  # Thư viện để load biến môi trường từ file .env
import streamlit as st  # Thư viện để tạo giao diện web
from crew.crew import WeeklyNewsUpdateCrew
# Load các biến môi trường từ file .env
load_dotenv()


class NewsletterGenUI:
    """
    Class chính để xử lý giao diện người dùng của ứng dụng tạo newsletter
    """

    def load_html_template(self):
        with open("src/newsletter_gen/config/newsletter_template.html", "r") as file:
            html_template = file.read()

        return html_template

    def generate_newsletter(self, topic, personal_message):
        inputs = {
            "topic": topic,
            "personal_message": personal_message,
            "html_template": self.load_html_template(),
        }
        return WeeklyNewsUpdateCrew().crew().kickoff(inputs=inputs)

    def newsletter_generation(self):

        if st.session_state.generating:
            st.session_state.newsletter = self.generate_newsletter(
                st.session_state.topic, st.session_state.personal_message
            )

        if st.session_state.newsletter and st.session_state.newsletter != "":
            with st.container():
                st.write("Newsletter generated successfully!")
                st.download_button(
                    label="Download HTML file",
                    data=st.session_state.newsletter,
                    file_name="newsletter.html",
                    mime="text/html",
                )
            st.session_state.generating = False

    def sidebar(self):
        """
        Tạo và quản lý thanh sidebar của ứng dụng
        Chứa các input và nút điều khiển chính
        """
        with st.sidebar:
            # Tiêu đề của sidebar
            st.title("Newsletter Generator")

            # Mô tả ngắn về cách sử dụng
            st.write(
                """
                To generate a newsletter, enter a topic and a personal message. \n
                Your team of AI agents will generate a newsletter for you!
                """
            )

            # Input field cho chủ đề newsletter
            st.text_input("Topic", key="topic", placeholder="USA Stock Market")

            # Input field cho lời nhắn cá nhân
            st.text_area(
                "Your personal message (to include at the top of the newsletter)",
                key="personal_message",
                placeholder="Dear readers, welcome to the newsletter!",
            )

            # Nút để bắt đầu tạo newsletter
            if st.button("Generate Newsletter"):
                st.session_state.generating = True

    def render(self):
        """
        Hàm chính để render toàn bộ giao diện ứng dụng
        Khởi tạo các biến session state và hiển thị các thành phần UI
        """
        # Cấu hình trang Streamlit
        st.set_page_config(page_title="Newsletter Generation", page_icon="📧")

        # Khởi tạo các biến trong session_state nếu chưa tồn tại
        if "topic" not in st.session_state:
            st.session_state.topic = ""

        if "personal_message" not in st.session_state:
            st.session_state.personal_message = ""

        if "newsletter" not in st.session_state:
            st.session_state.newsletter = ""

        if "generating" not in st.session_state:
            st.session_state.generating = False

        # Hiển thị sidebar
        self.sidebar()

        # Tạm thời comment out phần tạo newsletter
        #self.newsletter_generation()


# Entry point của ứng dụng
if __name__ == "__main__":
    NewsletterGenUI().render()  # Khởi tạo và hiển thị giao diện