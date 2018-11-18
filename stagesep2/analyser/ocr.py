import platform
import subprocess
import tempfile
import os
import cv2
import uuid

from stagesep2.analyser.base import BaseAnalyser
from stagesep2.config import OCRConfig, NormalConfig


class OCRAnalyser(BaseAnalyser):
    """ ocr analyser """
    name = 'ocr'

    @staticmethod
    def is_windows():
        return platform.system() == 'Windows'

    @classmethod
    def exec_tesseract(cls, src, dst):
        cmd = ['tesseract', src, dst, '-l', OCRConfig.lang]
        need_shell = cls.is_windows()
        tesseract_process = subprocess.Popen(
            cmd,
            shell=need_shell,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        tesseract_process.communicate(timeout=5)
        if tesseract_process.returncode:
            error_msg = tesseract_process.stderr.read()
            raise RuntimeError('tesseract error: {}'.format(error_msg))

    @classmethod
    def run(cls, frame):
        """
        run ocr analyser

        1. write frame to file
        2. execute tesseract to analyse it
        3. and get its result
        4. delete temp file and return result

        :param frame:
        :return:
        """
        # create temp picture file
        temp_pic = tempfile.NamedTemporaryFile(delete=False, suffix='.png')
        temp_pic_path = temp_pic.name
        temp_pic.close()
        # tesseract will auto create result file
        # and add '.txt' after its name!
        temp_result_path = os.path.join(NormalConfig.PROJECT_PATH, str(uuid.uuid1()))
        real_temp_result_path = temp_result_path + '.txt'

        # write in
        cv2.imwrite(temp_pic_path, frame)
        # execute tesseract
        cls.exec_tesseract(temp_pic_path, temp_result_path)
        # get result
        with open(real_temp_result_path, encoding='utf-8') as result_file:
            result = result_file.read()
        # remove temp files
        os.remove(temp_pic_path)
        os.remove(real_temp_result_path)
        return result