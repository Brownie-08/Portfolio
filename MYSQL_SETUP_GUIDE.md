# MySQL Setup Guide for Portfolio Project

## Step 1: Install MySQL on Windows

### Option A: MySQL Installer (Recommended)
1. Download MySQL Installer from https://dev.mysql.com/downloads/installer/
2. Run the installer and choose "Developer Default" setup
3. Follow the installation wizard
4. Set up a root password (remember this!)
5. Configure MySQL as a Windows Service

### Option B: XAMPP (Alternative)
1. Download XAMPP from https://www.apachefriends.org/
2. Install XAMPP with MySQL component
3. Start MySQL from XAMPP Control Panel

## Step 2: Create Portfolio Database

Open MySQL Command Line Client or phpMyAdmin and run:

```sql
CREATE DATABASE portfolio_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'portfolio_user'@'localhost' IDENTIFIED BY 'your_secure_password';
GRANT ALL PRIVILEGES ON portfolio_db.* TO 'portfolio_user'@'localhost';
FLUSH PRIVILEGES;
```

## Step 3: Configure Environment Variables

Create or update your `.env` file with:

```env
# MySQL Database Configuration
DB_ENGINE=django.db.backends.mysql
DB_NAME=portfolio_db
DB_USER=portfolio_user
DB_PASSWORD=your_secure_password
DB_HOST=localhost
DB_PORT=3306

# Or use a single DATABASE_URL (alternative)
# DATABASE_URL=mysql://portfolio_user:your_secure_password@localhost:3306/portfolio_db
```

## Step 4: Install Required Python Packages

The `mysqlclient` package is already in requirements.txt. If you encounter issues, try:

```bash
pip install mysqlclient
```

For Windows, if you get compilation errors, try:
```bash
pip install mysqlclient --only-binary=all
```

## Step 5: Run Migrations

After setting up MySQL:

```bash
python manage.py makemigrations
python manage.py migrate
```

## Step 6: Import Existing Data

If you have existing SQLite data to preserve:

```bash
# Dump SQLite data
python manage.py dumpdata --format=json > backup_data.json

# After switching to MySQL and running migrations
python manage.py loaddata backup_data.json
```

## Troubleshooting

### MySQL Connection Issues
- Ensure MySQL service is running
- Check firewall settings
- Verify database credentials
- Test connection with MySQL client

### Python mysqlclient Issues on Windows
1. Install Microsoft C++ Build Tools
2. Or use alternative: `pip install PyMySQL` and add to settings:
   ```python
   import pymysql
   pymysql.install_as_MySQLdb()
   ```

### Common Errors
- **Error 1045**: Access denied - Check username/password
- **Error 2003**: Can't connect - Check if MySQL is running
- **Error 1049**: Unknown database - Ensure database exists

## Production Considerations

For production deployment:
- Use environment-specific database credentials
- Enable SSL connections
- Set up database backups
- Configure connection pooling
- Monitor database performance

## Database Optimization

After migration, consider:
- Adding appropriate indexes
- Configuring MySQL settings for your workload
- Setting up connection pooling
- Monitoring query performance
