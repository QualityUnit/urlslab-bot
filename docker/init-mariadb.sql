CREATE DATABASE IF NOT EXISTS `urlslab-bot`;
CREATE DATABASE IF NOT EXISTS `urlslab-bot-user`;

GRANT ALL PRIVILEGES ON `urlslab-bot`.* TO 'urlslab-bot'@'%';
GRANT ALL PRIVILEGES ON `urlslab-bot-user`.* TO 'urlslab-bot'@'%';