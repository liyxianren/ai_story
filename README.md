# AI Storytelling Project - Database Setup

This project tests MySQL database connectivity for a Python web application.

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

You need to set these environment variables for your Zeabur MySQL database:

```bash
export PORT_FORWARDED_HOSTNAME=your-actual-hostname
export DATABASE_PORT_FORWARDED_PORT=your-actual-port
```

**Or create a `.env` file** in the project root with:

```
PORT_FORWARDED_HOSTNAME=your-actual-hostname
DATABASE_PORT_FORWARDED_PORT=your-actual-port
```

### 3. Test Database Connection

Run the test script:

```bash
python test_db_connection.py
```

## Database Connection Details

- **Host**: ${PORT_FORWARDED_HOSTNAME} (environment variable)
- **Port**: ${DATABASE_PORT_FORWARDED_PORT} (environment variable)
- **Username**: root
- **Password**: 69uc42U0oG7Js5Cm831ylixRqHODwXLI
- **Database**: zeabur

## What the Test Does

The `test_db_connection.py` script will:

1. ✅ Connect to your MySQL database
2. ✅ Show database version and server info
3. ✅ List all tables in the database
4. ✅ Verify the connection is working properly

## Next Steps

Once the database connection test passes, you can proceed with building your Python web application! 