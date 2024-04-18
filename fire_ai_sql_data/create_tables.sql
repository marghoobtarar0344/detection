USE AIHUMANPETROL
-- drop table LUCY_TO_UI
-- DROP table content_type
-- drop table frames
-- drop table video_path_table
-- drop TABLE Cameras
-- DROP TABLE LUCY_TO_PROCESS_CLAC
-- DROP table metrices
-- DROP TABLE sample_random_frame
-- drop TABLE perform_task
-- drop TABLE events_occur
-- drop TABLE sms_verification

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Cameras](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[camera_link] [varchar](255) NOT NULL,
	[x_axis] [float] NOT NULL,
	[y_axis] [float] NOT NULL,
	[camera_name] [varchar](255) NULL,
	[current_status] [bit] NULL,
	[stop_it] [bit] NULL,
	[type] [varchar](255) NULL,
	[elevation] [float] NULL,
	[bearing] [float] NULL,
	[error_status] bit 0,
	[error_description] [varchar](255) NULL,
	[control_comment] [varchar](max) NULL,
	[quality_status] [bit] NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[Cameras] ADD  CONSTRAINT [PK_Cameras] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Cameras] ADD  DEFAULT ((0)) FOR [current_status]
GO
ALTER TABLE [dbo].[Cameras] ADD  DEFAULT ((0)) FOR [stop_it]
GO
ALTER TABLE [dbo].[Cameras] ADD  DEFAULT ((0)) FOR [elevation]
GO
ALTER TABLE [dbo].[Cameras] ADD  DEFAULT ((0)) FOR [bearing]
GO

DBCC CHECKIDENT ('[dbo].[Cameras]', RESEED, 0);
GO

GO
	CREATE TABLE [dbo].[video_path_table](
		[ID] [int] IDENTITY(1, 1) NOT NULL,
		[main_file] [int]  NOT NULL,
		[folder_path] [varchar] (255) NOT NULL,
	)
	
ALTER TABLE [dbo].[video_path_table]
ADD sample_flag [varchar](50)

ALTER TABLE
		[dbo].[video_path_table] WITH CHECK
	ADD
		CONSTRAINT [main_file] FOREIGN KEY([main_file]) REFERENCES [dbo].[Cameras] ([ID]) ON UPDATE CASCADE ON DELETE CASCADE
	GO
ALTER TABLE
	[dbo].[video_path_table]
ADD
	CONSTRAINT [PK_video_path_table] PRIMARY KEY CLUSTERED ([ID] ASC) WITH (
		PAD_INDEX = OFF,
		STATISTICS_NORECOMPUTE = OFF,
		IGNORE_DUP_KEY = OFF,
		ONLINE = OFF,
		ALLOW_ROW_LOCKS = ON,
		ALLOW_PAGE_LOCKS = ON
	) ON [PRIMARY]
GO
	CREATE TABLE [dbo].[frames](
		[ID] [int] IDENTITY(1, 1) NOT NULL,
		[video_path_table_id] [int] NOT NULL,
		[image_name] [varchar](100) NOT NULL,
		
		[presigned_url] [varchar](500) NULL,
		[content] [bit] DEFAULT 0,
		[is_read] [bit] DEFAULT 0,
		[frame_number] [bigint] NOT NULL,
		[time_in_sec]  DATETIME NOT NULL DEFAULT GETUTCDATE()
	)
ALTER TABLE
	[dbo].[frames]
ADD
	CONSTRAINT [PK_frames] PRIMARY KEY CLUSTERED ([ID] ASC) WITH (
		PAD_INDEX = OFF,
		STATISTICS_NORECOMPUTE = OFF,
		IGNORE_DUP_KEY = OFF,
		ONLINE = OFF,
		ALLOW_ROW_LOCKS = ON,
		ALLOW_PAGE_LOCKS = ON
	) ON [PRIMARY]
ALTER TABLE
	[dbo].[frames] WITH CHECK
ADD
	CONSTRAINT [FK_frames_video_path_table_id] FOREIGN KEY([video_path_table_id]) REFERENCES [dbo].[video_path_table] ([ID]) ON UPDATE CASCADE ON DELETE CASCADE
GO
ALTER TABLE
	[dbo].[frames] CHECK CONSTRAINT [FK_frames_video_path_table_id]
GO
 ALTER TABLE
	[frames]
ADD
	[detection_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE();

GO
 ALTER TABLE
	[frames]
ADD
	[current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE();

GO


GO

GO
		CREATE TABLE [dbo].[content_type](
			[ID] [int] IDENTITY(1, 1) NOT NULL,
			[frame_table_id] [int] NOT NULL,
			[score] [float] NOT NULL,
			[category] [varchar](50) NOT NULL,
			[x_min] [float] NOT NULL,
			[y_min] [float] NOT NULL,
			[x_max] [float] NOT NULL,
			[y_max] [float] NOT NULL,
			[area] [float] NULL,
			[area_percentage]  AS (((([x_max]-[x_min])*([y_max]-[y_min]))*(100))/((640)*(640))),
		)
	ALTER TABLE
		[dbo].[content_type]
	ADD
		CONSTRAINT [PK_content_type] PRIMARY KEY CLUSTERED ([ID] ASC) WITH (
			PAD_INDEX = OFF,
			STATISTICS_NORECOMPUTE = OFF,
			IGNORE_DUP_KEY = OFF,
			ONLINE = OFF,
			ALLOW_ROW_LOCKS = ON,
			ALLOW_PAGE_LOCKS = ON
		) ON [PRIMARY]
	ALTER TABLE
		[dbo].[content_type] WITH CHECK
	ADD
		CONSTRAINT [FK_frame_table_id] FOREIGN KEY([frame_table_id]) REFERENCES [dbo].[frames] ([ID]) ON UPDATE CASCADE ON DELETE CASCADE
	GO
	ALTER TABLE
		[dbo].[content_type] CHECK CONSTRAINT [FK_frame_table_id]
	GO

GO	
  ALTER TABLE
	[content_type]
ADD
	[current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE()

GO

	
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[sample_random_frame](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[category] [varchar](max) NULL,
	[frame_ID] [bigint] NOT NULL,
	[frame_number] [bigint] NOT NULL,
	[image_name] [varchar](max) NOT NULL,
 CONSTRAINT [PK_sample_random_frame] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

CREATE TABLE [dbo].[perform_task](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[process] [varchar](max) NULL,
	[processed_code] [bigint] NULL,
	[counter_is] [bigint] NULL
 CONSTRAINT [PK_perform_task] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
INSERT INTO perform_task (process,processed_code,counter_is) VALUES('modeling',422,1)

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[LUCY_TO_UI](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[frame_table_id] [int] NOT NULL,
	[feedback] [varchar](max) NULL,
	[given_x_min] [float] NULL,
	[given_y_min] [float] NULL,
	[given_x_max] [float] NULL,
	[given_y_max] [float] NULL,
	[category] [bit] NULL,
 CONSTRAINT [PK_LUCY_TO_UI] PRIMARY KEY CLUSTERED 
(
	[ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
ALTER TABLE [dbo].[LUCY_TO_UI] ADD  DEFAULT ((-1)) FOR [given_x_min]
GO
ALTER TABLE [dbo].[LUCY_TO_UI] ADD  DEFAULT ((-1)) FOR [given_y_min]
GO
ALTER TABLE [dbo].[LUCY_TO_UI] ADD  DEFAULT ((-1)) FOR [given_x_max]
GO
ALTER TABLE [dbo].[LUCY_TO_UI] ADD  DEFAULT ((-1)) FOR [given_y_max]
GO
ALTER TABLE [dbo].[LUCY_TO_UI] ADD  DEFAULT ((0)) FOR [category]
GO
ALTER TABLE [dbo].[LUCY_TO_UI]  WITH CHECK ADD  CONSTRAINT [FK_LUCY_TO_UI] FOREIGN KEY([frame_table_id])
REFERENCES [dbo].[frames] ([ID])
ON UPDATE CASCADE
ON DELETE CASCADE
GO
ALTER TABLE [dbo].[LUCY_TO_UI] CHECK CONSTRAINT [FK_LUCY_TO_UI]
GO
	
GO
        CREATE TABLE [dbo].[LUCY_TO_PROCESS_CLAC](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
            [Camera_ID] [int] NOT NULL,
            [Location_ID] [varchar](max)  NULL,
            [image_name] [varchar] (255) NULL,
            [image_path] [varchar] (255) NULL,
            [processed_flag] [bit] DEFAULT 0,
            [prediction_flag] [bit]  NULL,
            [feedback_loop] [int]  NULL,
            [current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE()
            CONSTRAINT [PK_LUCY_TO_PROCESS_CLAC] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]

CREATE NONCLUSTERED INDEX IX_LUCY_TO_PROCESS_CLAC ON [dbo].[LUCY_TO_PROCESS_CLAC] ([current_datetime]);

GO

GO
    CREATE TABLE [dbo].[events_occur](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
            [event_name] [varchar](max) NOT NULL,
            [is_completed]  [int] DEFAULT 0,
			[is_started] [int] DEFAULT 0,
            [description] [varchar](max)  NULL,
			[is_read] [int] DEFAULT 0,
           
            CONSTRAINT [PK_events_occur] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

GO
    CREATE TABLE [dbo].[sms_verification](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
            [code]  [int] NOT NULL,
            [from_number] [varchar](max)  NULL,
            [to_number] [varchar](max)  NULL,
			[current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT [PK_sms_verification] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO

GO
    CREATE TABLE [dbo].[metrices](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
           
 [DetectionBoxes_Precision_mAP]  [float] DEFAULT 0 ,
            [DetectionBoxes_Precision_mAP_75IOU]  [float] DEFAULT 0 ,
            [DetectionBoxes_Precision_mAP_50IOU]  [float] DEFAULT 0 ,
            [DetectionBoxes_Precision_mAP_small]  [float] DEFAULT 0 ,
            [DetectionBoxes_Precision_mAP_medium]  [float] DEFAULT 0 ,
            [DetectionBoxes_Precision_mAP_large]  [float] DEFAULT 0 ,
            [DetectionBoxes_Recall_AR_1]  [float] DEFAULT 0 ,
            [DetectionBoxes_Recall_AR_10]  [float] DEFAULT 0 ,
            [DetectionBoxes_Recall_AR_100]  [float] DEFAULT 0 ,
            [DetectionBoxes_Recall_AR_100_small]  [float] DEFAULT 0 ,
            [DetectionBoxes_Recall_AR_100_medium]  [float] DEFAULT 0 ,
            [DetectionBoxes_Recall_AR_100_large]  [float] DEFAULT 0 ,
            [Loss_localization_loss]  [float] DEFAULT 0 ,
            [Loss_classification_loss]  [float] DEFAULT 0 ,
            [Loss_regularization_loss]  [float] DEFAULT 0 ,
            [Loss_total_loss] [float] DEFAULT 0 ,
			[current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT [PK_metrices] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO

GO
        CREATE TABLE [dbo].[AUDIT_FRAMES_CALCULATION](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
            [Camera_ID] [int] NOT NULL,
            [total_frames] [int]  DEFAULT 0,
            [have_content] [int]  DEFAULT 0,
            [no_content] [int] DEFAULT 0,
            [is_processing] [bit] DEFAULT 0,
            [processed_successfully] [bit]  DEFAULT 0,
            [passed] [int]  DEFAULT 0,
            [current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE()
            CONSTRAINT [PK_AUDIT_FRAMES_CALCULATION] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO

SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[alert](
	[AlertUrl] [nvarchar](450) NOT NULL,
	[FireLocation] [geography] NOT NULL,
	[DetectionTime] [datetime2](7) NOT NULL,
	[CameraID] [int] NOT NULL,
	[CameraName] [nvarchar](max) NULL,
	[CameraDetails] [nvarchar](max) NULL,
	[GDA94Coordinates] [geography] NULL,
	[ConfidenceScore] [real] NOT NULL,
	[DetectionImageUrl] [nvarchar](max) NULL,
	[Bearing] [real] NOT NULL,
	[FireShape] [geography] NULL,
	[SearchAreaRadius] [decimal](18, 2) NOT NULL,
	[GridReference] [nvarchar](max) NOT NULL,
	[FrameNumber] [int] NOT NULL
) ON [PRIMARY] TEXTIMAGE_ON [PRIMARY]
GO
SET ANSI_PADDING ON
GO
ALTER TABLE [dbo].[alert] ADD  CONSTRAINT [PK_BushfireDetection] PRIMARY KEY CLUSTERED 
(
	[AlertUrl] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, SORT_IN_TEMPDB = OFF, IGNORE_DUP_KEY = OFF, ONLINE = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
GO
/****** Object:  Table [dbo].[NOTIFICATION_THRESHOLD]    Script Date: 6/27/2023 11:27:58 AM ******/
SET ANSI_NULLS ON



GO
    CREATE TABLE [dbo].[notification_reasoning](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
            [reason]  [varchar] (200) NOT NULL,
            [frame_number] [int] NOT  NULL,
            [generate_alarm] [bit] NOT NULL,
            [current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT [PK_notification_rules] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO
ALTER TABLE
		[dbo].[notification_reasoning] WITH CHECK
	ADD
		CONSTRAINT [FK_notification_reasoning_frame_number] FOREIGN KEY([frame_number]) REFERENCES [dbo].[frames] ([ID]) ON UPDATE CASCADE ON DELETE CASCADE
	GO


GO
    CREATE TABLE [dbo].[camera_logs](
            [ID] [int] IDENTITY(1, 1) NOT NULL,
            [camera_id] [int] NOT  NULL,
			[status] [bit] NOT NULL,
            [description]  [varchar](200) NOT NULL,
  			[current_datetime] DATETIME NOT NULL DEFAULT GETUTCDATE(),
            CONSTRAINT [PK_camera_logs] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
GO
ALTER TABLE
		[dbo].[camera_logs] WITH CHECK
	ADD
		CONSTRAINT [FK_camera_logs_camera_id] FOREIGN KEY([camera_id]) REFERENCES [dbo].[Cameras] ([ID]) ON UPDATE CASCADE ON DELETE CASCADE
	GO


GO
	CREATE TABLE [dbo].[low_quality_images](
		[ID] [int] IDENTITY(1, 1) NOT NULL,
		[image_name] [varchar](100) NOT NULL,
		[presigned_url] [varchar](500) NULL,
		[file_size] [float] DEFAULT 0,
		[camera_logs_id] [int] NOT NULL,
		[current_datetime]  DATETIME NOT NULL DEFAULT GETUTCDATE()

	  CONSTRAINT [PK_low_quality_images] PRIMARY KEY CLUSTERED 
(
    [ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 
ALTER TABLE
	AIHUMAN.[dbo].[low_quality_images] WITH CHECK
ADD
CONSTRAINT [FK_low_quality_images_camera_logs_id] FOREIGN KEY([camera_logs_id]) REFERENCES AIHUMAN.[dbo].[camera_logs] ([ID]) ON UPDATE CASCADE ON DELETE CASCADE

GO


 GO
	CREATE TABLE [dbo].[notification_time_configurations](
		[ID] [int] IDENTITY(1, 1) NOT NULL,
		[customer_id] [varchar](100) NOT NULL,
		[start_date]  DATETIME NOT NULL DEFAULT GETUTCDATE(),
		[end_date]  DATETIME NOT NULL DEFAULT GETUTCDATE(),
		[daily_monitor_start_time] TIME NOT NULL DEFAULT GETUTCDATE(),
		[daily_monitor_end_time]  TIME NOT NULL DEFAULT GETUTCDATE(),
		[created_date]  DATETIME NOT NULL DEFAULT GETUTCDATE(),
		[deleted_date]  DATETIME  NULL,
		[camera_id] [int] NOT NULL
			CONSTRAINT [PK_notification_time_configurations] PRIMARY KEY CLUSTERED 

(
	[ID] ASC
)WITH ( STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON) ON [PRIMARY]
) ON [PRIMARY] 

    GO
INSERT INTO AIHUMAN.[dbo].[notification_time_configurations]
(customer_id, start_date,end_date,daily_monitor_start_time,daily_monitor_end_time,camera_id )
VALUES
(10,'2023-12-25','2024-12-25','06:00:00','18:00:00',1077)


-- GO

-- SET QUOTED_IDENTIFIER ON
-- GO

-- CREATE TABLE [dbo].[NOTIFICATION_THRESHOLD](
-- 	[ID] [int] IDENTITY(1,1) NOT NULL,
-- 	[TIME_ELAPSED_IN_MINUTES] [float] NOT NULL,
-- 	[MAX_THRESHOLD_WITH_TIME_ELAPSED] [float] NULL,
-- 	[MIN_THRESHOLD_NO_TIME_ELAPSED] [float] NULL,
-- 	[AREA_PERCENTAGE_THRESHOLD] [float] NULL,
--  CONSTRAINT [PK_NOTIFICATION_THRESHOLD] PRIMARY KEY CLUSTERED 
-- (
-- 	[ID] ASC
-- )WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
-- ) ON [PRIMARY]
-- GO

-- ALTER TABLE [dbo].[NOTIFICATION_THRESHOLD] ADD  DEFAULT ((0)) FOR [MAX_THRESHOLD_WITH_TIME_ELAPSED]
-- GO

-- ALTER TABLE [dbo].[NOTIFICATION_THRESHOLD] ADD  DEFAULT ((0)) FOR [MIN_THRESHOLD_NO_TIME_ELAPSED]
-- GO

-- ALTER TABLE [dbo].[NOTIFICATION_THRESHOLD] ADD  DEFAULT ((10)) FOR [AREA_PERCENTAGE_THRESHOLD]
-- GO

-- INSERT INTO [dbo].[NOTIFICATION_THRESHOLD] (TIME_ELAPSED_IN_MINUTES,MAX_THRESHOLD_WITH_TIME_ELAPSED,MIN_THRESHOLD_NO_TIME_ELAPSED,AREA_PERCENTAGE_THRESHOLD)
-- VALUES (15,1.03,0.009,8)
