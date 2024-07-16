# BlogPostBackend

Setup Instructions

⦁	Clone/copy the code from repo 
⦁	Create a mongoDb
⦁	Run the command python run.py 
⦁	To test the API either Postman can be used or can use the frontend code above



API Calls
User Signup
API Name: /signup
Method: POST
Input Parameters:
⦁	username (string) - The desired username for the new user.
⦁	password (string) - The password for the new user.
Description: Registers a new user with a username and password.

User Login
API Name: /login
Method: POST
Input Parameters:
⦁	username (string) - The username of the user.
⦁	password (string) - The password of the user.
Description: Authenticates a user and provides a JWT token upon successful login for subsequent requests.
Upload Image
API Name: /upload-image
Method: POST
Input Parameters:
⦁	file (file) - The image file to be uploaded.
Description: Handles the upload of an image file and stores it in the server's upload folder.

Create Blog Post
API Name: /blogposts
Method: POST
Input Parameters:
⦁	title (string) - The title of the blog post.
⦁	content (string) - The content of the blog post.
⦁	file (file) - The image file to be uploaded (optional).
Description: Creates a new blog post with a title, content, and optionally an image.


Get All Blog Posts
API Name: /blogposts
Method: GET
Input Parameters: None
Description: Retrieves all blog posts from the database.

Get a Single Blog Post
API Name: /blogposts/<post_id>
Method: GET
Input Parameters:
⦁	post_id (string) - The ID of the blog post to retrieve.
Description: Retrieves a specific blog post by its ID.

Update Blog Post
API Name: /blogposts/<post_id>
Method: PUT
Input Parameters:
⦁	title (string) - The new title of the blog post.
⦁	content (string) - The new content of the blog post.
⦁	file (file) - The new image file to be uploaded (optional).
Description: Updates an existing blog post identified by its ID with a new title, content, and optionally a new image.

Delete Blog Post
API Name: /blogposts/<post_id>
Method: DELETE
Input Parameters:
⦁	post_id (string) - The ID of the blog post to delete.
Description: Deletes an existing blog post identified by its ID.

Design Decisions and Choices
Code Quality
⦁	Cleanliness and Readability:
⦁	Modular code divided into separate files for routes, models, and tests.
⦁	Consistent naming conventions and appropriate commenting enhance clarity.
⦁	Best Practices:
⦁	Follows good coding practices such as error handling, validation, and separation of concerns.
⦁	Functions are defined with single responsibilities, making the codebase easier to understand and extend.

RESTful Design
⦁	Resource-Based URLs:
⦁	URLs are designed to be resource-based, following RESTful conventions (e.g., /blogposts, /blogposts/<post_id>).
⦁	This makes the API intuitive and easy to use.
⦁	HTTP Methods:
⦁	Appropriate HTTP methods are used for different actions (GET, POST, PUT, DELETE), adhering to RESTful principles.
⦁	Statelessness:
⦁	The API is stateless, with each request containing all the information needed for processing, achieved using JWT for authentication.

System Architecture
⦁	Scalability:
⦁	The application is designed to be scalable, using Flask for easy deployment and scaling with various web servers and load balancers.
⦁	MongoDB can handle large volumes of data and can be scaled horizontally.
⦁	Maintainability:
⦁	Separation of concerns into different modules (routes, models) ensures easy maintenance and extension.
⦁	Each module handles a specific aspect of the application.
⦁	Extensibility:
⦁	Built with extensibility in mind, allowing new features to be added with minimal changes to the existing codebase.
Authentication
⦁	JWT:
⦁	JSON Web Tokens (JWT) are used for secure and scalable authentication, with tokens easily verified without server-side session storage.
⦁	Protected Routes:
⦁	Critical routes are protected using the @jwt_required() decorator, ensuring only authenticated users can access them.

Database Usage
⦁	Data Modeling:
⦁	Data models for User and BlogPost are defined to handle necessary fields, making the data structure clear and easy to manage.
⦁	Queries:
⦁	Efficient MongoDB queries are used for CRUD operations, optimized for performance.
⦁	Image Handling:
⦁	Handles image uploads and stores image URLs in MongoDB, ensuring blog posts can include images.

Testing
⦁	Unit Tests:
⦁	Comprehensive unit tests cover critical functionality, ensuring the application works as expected and helps catch bugs early.
⦁	Test Isolation:
⦁	Each test case starts with a clean state by dropping the collections, ensuring tests do not interfere with each other
Trade-Offs
⦁	Simplified Error Handling:
⦁	Error handling is implemented but could be more granular and detailed, keeping the code simple and focused on main functionality.
⦁	Minimal Validation:
⦁	Basic validation is implemented, but more comprehensive validation could improve data integrity.
Additional Features or Improvements with More Time
⦁	Enhanced Validation:
⦁	Implement more comprehensive validation using a library like Marshmallow to ensure data integrity and provide better error messages.
⦁	Improved Error Handling:
⦁	Add more detailed error handling and logging to help with debugging and provide more information to the client in case of errors.
⦁	Image Optimization:
⦁	Implement image resizing and optimization to improve performance and user experience.
⦁	Pagination:
⦁	Add pagination to the /blogposts endpoint to handle large datasets more efficiently.
⦁	Role-Based Access Control:
⦁	Introduce roles (e.g., admin, user) and permissions to provide finer control over actions different users can perform.
