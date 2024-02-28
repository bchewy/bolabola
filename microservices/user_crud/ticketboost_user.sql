DROP DATABASE IF EXISTS ticketboost_user;
CREATE DATABASE ticketboost_user;
USE ticketboost_user;

-- Create the User table
CREATE TABLE User (
    id INTEGER PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(80) NOT NULL,
    email VARCHAR(120) UNIQUE NOT NULL,
    stripe_id VARCHAR(120) UNIQUE,
    username VARCHAR(80) UNIQUE NOT NULL,
    password VARCHAR(120) NOT NULL
);

-- Insert dummy data for 10 users
INSERT INTO User (name, email, stripe_id, username, password)
VALUES
    ('John Doe', 'john@example.com', NULL, 'johndoe', 'password1'),
    ('Jane Smith', 'jane@example.com', NULL, 'janesmith', 'password2'),
    ('Alice Johnson', 'alice@example.com', NULL, 'alicej', 'password3'),
    ('Bob Brown', 'bob@example.com', NULL, 'bobbrown', 'password4'),
    ('Emily Davis', 'emily@example.com', NULL, 'emilyd', 'password5'),
    ('Michael Wilson', 'michael@example.com', NULL, 'michaelw', 'password6'),
    ('Sarah Taylor', 'sarah@example.com', NULL, 'saraht', 'password7'),
    ('David Martinez', 'david@example.com', NULL, 'davidm', 'password8'),
    ('Laura Anderson', 'laura@example.com', NULL, 'lauraa', 'password9'),
    ('James Lee', 'james@example.com', NULL, 'jamesl', 'password10'),
    ('王小明', 'wangxiaoming@example.com', NULL, 'wangxm', 'password11'),
    ('李芳', 'lifang@example.com', NULL, 'lif', 'password12'),
    ('张伟', 'zhangwei@example.com', NULL, 'zhangw', 'password13'),
    ('刘亮', 'liuliang@example.com', NULL, 'liul', 'password14'),
    ('陈丽', 'chenli@example.com', NULL, 'chenl', 'password15'),
    ('周健', 'zhoujian@example.com', NULL, 'zhouj', 'password16'),
    ('吴秀英', 'wuxiuying@example.com', NULL, 'wuxy', 'password17'),
    ('许伟', 'xuwei@example.com', NULL, 'xuw', 'password18'),
    ('孙莉', 'sunli@example.com', NULL, 'sunl', 'password19'),
    ('朱强', 'zhuqiang@example.com', NULL, 'zhuq', 'password20'),
    ('Ahmed Ali', 'ahmedali@example.com', NULL, 'ahmeda', 'password21'),
    ('Fatima Khan', 'fatimakhan@example.com', NULL, 'fatimak', 'password22'),
    ('Muhammad Rahman', 'muhammadrahman@example.com', NULL, 'muhammadr', 'password23'),
    ('Aisha Ahmed', 'aishaahmed@example.com', NULL, 'aishaa', 'password24'),
    ('Yusuf Abbas', 'yusufabbas@example.com', NULL, 'yusufa', 'password25'),
    ('Zainab Hassan', 'zainabhassan@example.com', NULL, 'zainabh', 'password26'),
    ('Safiya Hussain', 'safiyahussain@example.com', NULL, 'safiyah', 'password27'),
    ('Omar Malik', 'omarmalik@example.com', NULL, 'omarm', 'password28'),
    ('Layla Khan', 'laylakhan@example.com', NULL, 'laylak', 'password29'),
    ('Hamza Farooq', 'hamzafarooq@example.com', NULL, 'hamzaf', 'password30'),
    ('Amit Patel', 'amitpatel@example.com', NULL, 'amitp', 'password41'),
    ('Neha Sharma', 'nehasharma@example.com', NULL, 'nehas', 'password42'),
    ('Raj Singh', 'rajsingh@example.com', NULL, 'rajs', 'password43'),
    ('Deepak Gupta', 'deepakgupta@example.com', NULL, 'deepakg', 'password44'),
    ('Pooja Verma', 'poojaverma@example.com', NULL, 'poojav', 'password45'),
    ('Rahul Yadav', 'rahulyadav@example.com', NULL, 'rahuly', 'password46'),
    ('Anjali Mishra', 'anjalimishra@example.com', NULL, 'anjalim', 'password47'),
    ('Vikram Singh', 'vikramsingh@example.com', NULL, 'vikrams', 'password48'),
    ('Aarti Kumari', 'aartikumari@example.com', NULL, 'aartik', 'password49'),
    ('Ravi Tiwari', 'ravitiwari@example.com', NULL, 'ravit', 'password50');
