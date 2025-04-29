from ftplib import FTP

import core.config.config as cfg


def ftp_connect() -> FTP():
    ftp = FTP()
    ftp.connect(host=cfg.FTP_HOST, port=cfg.FTP_PORT, timeout=30)
    ftp.login(user=cfg.FTP_LOGIN, passwd=cfg.FTP_PASSWORD)
    ftp.nlst()
    return ftp


def get_files_list() -> list[str]:
    ftp_conn = ftp_connect()
    ftp_conn.cwd(cfg.FTP_DIR_NAME)
    files = ftp_conn.nlst()
    ftp_conn.quit()
    return files
