-- USE [AuditLogDB]
-- GO
-- DROP TABLE IF EXISTS [dbo].[_NRT_CONFIG_DETAILS]

-- GO

-- Create table _NRT_CONFIG_DETAILS
-- ([ID] [int] IDENTITY(1,1) NOT NULL,
-- CREATE_DATE datetime DEFAULT(getdate()),
-- FILE_NAME VARCHAR(100),
-- PATH_FILE VARCHAR(100), 
-- PARAM VARCHAR(100),
-- VALUE_MAX VARCHAR(100),
-- VALUE_MIN VARCHAR(100)
-- );
-- GO

-- -- the hardcoded config threshold data

-- INSERT [dbo].[_NRT_CONFIG_DETAILS] ([FILE_NAME],[PATH_FILE],[PARAM],[VALUE_MAX],[VALUE_MIN]) VALUES ('global_variables.py','module_1/app/config','MAKE_MODEL_PROB_THRESHOLD',10,1)
-- INSERT [dbo].[_NRT_CONFIG_DETAILS] ([FILE_NAME],[PATH_FILE],[PARAM],[VALUE_MAX],[VALUE_MIN]) VALUES ('global_variables.py','module_1/app/config','COLOR_PROB_THRESHOLD',10,1)
-- INSERT [dbo].[_NRT_CONFIG_DETAILS] ([FILE_NAME],[PATH_FILE],[PARAM],[VALUE_MAX],[VALUE_MIN]) VALUES ('global_variables.py','module_1/app/config','COLOR2_PROB_THRESHOLD',10,1)
-- INSERT [dbo].[_NRT_CONFIG_DETAILS] ([FILE_NAME],[PATH_FILE],[PARAM],[VALUE_MAX],[VALUE_MIN]) VALUES ('global_variables.py','module_1/app/config','MAKE_MODEL_PROB_THRESHOLD',10,1)