import pytest


@pytest.fixture
def client():
    from src import app

    app.app.config['TESTING'] = True
    
    with app.app.app_context():

        with app.db.engine.begin() as connection:
            from sqlalchemy import text
            connection.execute(text('DROP TABLE IF EXISTS `event`;'))

            connection.execute(text('''CREATE TABLE `event` (
                `event_id` int NOT NULL AUTO_INCREMENT,
                `event_name` varchar(64) NOT NULL,
                `venue` varchar(64) NOT NULL,
                `entry_fee` float NOT NULL,
                `description` varchar(64) NOT NULL,
                `capacity` int NOT NULL,
                `slots_left` int NOT NULL,
                `time` timestamp NOT NULL,
                PRIMARY KEY (`event_id`)
                ) ENGINE=InnoDB DEFAULT CHARSET=utf8;'''))

            connection.execute(text('''INSERT INTO `event` VALUES (1,'Music Concert','City Hall',50,'An evening of classical music with a live orchestra.',50,50,'2024-12-25 19:00:00');'''))

    return app.app.test_client()
