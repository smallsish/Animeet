import pytest

@pytest.fixture
def client():
    from src import app

    app.app.config['TESTING'] = True

    with app.app.app_context():

        with app.db.engine.begin() as connection:
            from sqlalchemy import text
            
            connection.execute(text('DROP TABLE IF EXISTS `group_user`;'))
            connection.execute(text('DROP TABLE IF EXISTS `group`;'))

            connection.execute(text('''
                CREATE TABLE `group` ( 
                `group_id` int NOT NULL AUTO_INCREMENT, 
                `event_id` int NOT NULL, 
                `name` varchar(32) NOT NULL, 
                `max_capacity` int NOT NULL, 
                `slots_left` int NOT NULL, 
                `description` varchar(64) NOT NULL, 
                PRIMARY KEY (`group_id`) ) 
                ENGINE=InnoDB AUTO_INCREMENT=28 DEFAULT CHARSET=utf8; 
            '''))

            connection.execute(text('''INSERT INTO `group` (`event_id`, `name`, `max_capacity`, `slots_left`, `description`) 
                                    VALUES (1, 'Cosplay Enthusiasts', 5, 3, 'Group for cosplay lovers'),
                                    (2, 'Testing Enthusiasts', 15, 14, 'Group for testing lovers');
            '''))

            connection.execute(text('''CREATE TABLE `group_user` (
                `group_id` int NOT NULL,
                `user_id` int NOT NULL,
                `role` varchar(32) NOT NULL,
                `date_joined` datetime NOT NULL,
                `payment_status` varchar(16) NOT NULL,
                PRIMARY KEY (`group_id`, `user_id`),
                FOREIGN KEY (`group_id`) REFERENCES `group`(`group_id`) ON DELETE CASCADE
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
            '''))
            
            connection.execute(text('''INSERT INTO `group_user` VALUES (28, 1000, 'leader', '2024-09-28 10:32:12', 'unpaid'),
                                    (28, 1001, 'member', '2024-09-30 11:39:18', 'unpaid'),
                                    (29, 1002, 'leader', '2024-09-28 21:02:44', 'unpaid');


            '''))
            
            

    return app.app.test_client()

