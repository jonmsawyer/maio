Del /A filestore\media\images\*
Del /A filestore\thumbnails\*
FOR /D %%p IN ("filestore\media\images\*.*") DO rmdir "%%p" /s /q
FOR /D %%p IN ("filestore\thumbnails\*.*") DO rmdir "%%p" /s /q
