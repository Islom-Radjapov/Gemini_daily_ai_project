# My Social Profile Page

This is a small, interactive, and fully functional social media profile page implemented as a single HTML file. It showcases a user's profile information, statistics, navigation tabs, and a grid of example posts with like functionality. The design is modern and responsive, ensuring a good experience across various device sizes.

## Features:
*   **Responsive Design:** The layout gracefully adapts to different screen sizes, from desktop to mobile phones, using CSS media queries and Flexbox/Grid.
*   **Profile Header:** Displays a circular profile picture, user's name, unique username, and a concise bio.
*   **Interactive Buttons:**
    *   **Follow Button:** This button dynamically toggles between "Follow" and "Following" states upon click. It also updates the displayed follower count in real-time.
    *   **Like Button:** Each post features a like button that changes its visual state (color) and increments/decrements the like count when clicked.
    *   **Message Button:** A functional, styled button to simulate initiating a message (no backend integration in this small project).
*   **Profile Statistics:** Clearly presents the number of posts, followers, and users being followed.
*   **Tabbed Navigation:** Allows users to switch between different content categories ("Posts", "Photos", and "Saved"). The active tab is visually highlighted. (Note: Only the "Posts" tab contains actual content; "Photos" and "Saved" sections display an "empty state" message.)
*   **Posts Grid:** A responsive grid layout for displaying example posts, each featuring an image, a short caption, and interactive action buttons.
*   **Modern UI:** Built with clean, contemporary design principles, utilizing HTML5, CSS3 for styling, and vanilla JavaScript for interactivity, all contained within a single file.

## How to Run:
1.  **Save the HTML:** Copy the entire content provided for `my_profile_page.html` and save it into a new file named `my_profile_page.html` on your computer.
2.  **Open in Browser:** Navigate to the saved `my_profile_page.html` file on your computer and open it using any modern web browser (e.g., Google Chrome, Mozilla Firefox, Apple Safari, Microsoft Edge).
3.  **Interact:** The profile page will load immediately. You can now interact with the "Follow" button, click "Like" on any post, and switch between the "Posts", "Photos", and "Saved" navigation tabs to see the dynamic behavior.

## Project Structure:
The entire project is self-contained within a single file: `my_profile_page.html`.
*   **HTML:** Defines the semantic structure and content of the social profile page.
*   **CSS (`<style>` tag):** All styling rules, including responsive design adaptations for various screen sizes, are embedded directly within the `<style>` tag in the HTML head.
*   **JavaScript (`<script>` tag):** All interactive functionalities, such as managing the follow button's state and follower count, handling post likes, and switching content based on tab navigation, are implemented with vanilla JavaScript within the `<script>` tag at the end of the HTML body.