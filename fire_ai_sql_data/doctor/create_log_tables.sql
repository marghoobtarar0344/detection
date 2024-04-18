USE AuditLogDB 
DROP TABLE IF EXISTS [dbo].[BatchStatus]
GO
	DROP TABLE IF EXISTS [dbo].[AuditLog]
GO
	CREATE TABLE [dbo].[AuditLog](
		[id] [int] IDENTITY(1, 1) NOT NULL,
		[parent_process_name] [nvarchar](100) NOT NULL ,
        [child_process_name] [nvarchar](100) NOT NULL,
		[error_type] [nvarchar](100) NULL,
		[file_name] [nvarchar](100) NULL,
		[line_number] [nvarchar](100) NULL,
		[status] [nvarchar](100) NULL,
		[description] [nvarchar](500) NULL,
		[created_at] DATETIME DEFAULT CURRENT_TIMESTAMP,
		CONSTRAINT [PK_AuditLog_model_lookup] PRIMARY KEY CLUSTERED ([id] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON
		) ON [PRIMARY]
	) ON [PRIMARY] 
GO
	drop table if exists [dbo].[BatchStatus] CREATE TABLE [dbo].[BatchStatus](
		[id] [int] IDENTITY(1, 1) NOT NULL,
		[parent_process_name] [nvarchar](50) NOT NULL,
		[child_process_name] [nvarchar](50) NOT NULL,
		[server_credentials] [nvarchar](200) NOT NULL,
		[process_database] [nvarchar](200) NULL,
		[process_table] [nvarchar](50) NULL,
		[column_check_flag] [nvarchar](50) NULL, -- this is the column in the corresponding table which will be check as a flag
		[NRT_BATCH_STATUS] [nvarchar](10) NULL,
		[created_at] DATETIME DEFAULT CURRENT_TIMESTAMP,
		CONSTRAINT [PK_BatchStatus_model_lookup] PRIMARY KEY CLUSTERED ([id] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON
		) ON [PRIMARY]
	) ON [PRIMARY]
GO
SET
	IDENTITY_INSERT [dbo].[BatchStatus] ON -- MUST RUN THE INSERT STATEMENT
INSERT INTO
	[dbo].[BatchStatus] (
		id,
		parent_process_name,
		child_process_name,
		process_database,
		process_table,
		server_credentials,
		column_check_flag
	)
VALUES
	(
		1,
		'LUCY',
		'prediction',
		'[AIHUMAN]',
		'[dbo].[LUCY_TO_PROCESS_CLAC]',
		'DRIVER=ODBC Driver 17 for SQL Server;SERVER=192.168.50.183,1433;UID=sa;PWD=Iforgot@123',
		'processed_flag'
	)
INSERT INTO
	[dbo].[BatchStatus] (
		id,
		parent_process_name,
		child_process_name,
		process_database,
		process_table,
		server_credentials,
		column_check_flag
	)
VALUES
	(
		2,
		'LUCY',
		'camera',
		'[AIHUMAN]',
		'[dbo].[Cameras]',
		'DRIVER=ODBC Driver 17 for SQL Server;SERVER=192.168.50.183,1433;UID=sa;PWD=Iforgot@123',
		'current_status'
	)
INSERT INTO
	[dbo].[BatchStatus] (
		id,
		parent_process_name,
		child_process_name,
		server_credentials
	)
VALUES
	(
		3,
		'LUCY',
		'va_kafka',
		'DRIVER=ODBC Driver 17 for SQL Server;SERVER=192.168.50.183,1433;UID=sa;PWD=Iforgot@123'
	)