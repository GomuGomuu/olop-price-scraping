from app import OCR_PATH


class TesseractService:
    def __init__(self, cmd: str = None):
        import pytesseract

        self.tesseract = pytesseract
        self.cmd = OCR_PATH if cmd is None else cmd
        self.set_tesseracts_cmd()

    def set_tesseracts_cmd(self):
        self.tesseract.pytesseract.tesseract_cmd = self.cmd
