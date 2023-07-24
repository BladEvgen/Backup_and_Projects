import random
import cv2
import os


class OpenCv:
    """Обёртка над библиотекой OpenCV."""

    @staticmethod
    def read_image(file_path: str):
        print("file_path: ", file_path)
        # поиск файла
        file = cv2.samples.findFile(file_path)
        # чтение файла в матрицу(BGR==RGB)
        img = cv2.imread(file)
        return img

    @staticmethod
    def show_image(img: any):
        cv2.imshow(f"Display window{random.randint(1, 10000)}", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    @staticmethod
    def update_image(
        img: any,
        path_to_save_images,
        prefix_to_images,
        quality_for_save,
        is_gray,
        multiply,
    ):
        height, width, channels = img.shape  # (1920, 1080, 3)
        new_file_path = f"{path_to_save_images}{prefix_to_images}"
        if is_gray:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        multiply_val: float = multiply / 100  # 1.0 = 100%
        img = cv2.resize(img, (int(width * multiply_val), int(height * multiply_val)))
        cv2.imwrite(new_file_path, img, [cv2.IMWRITE_JPEG_QUALITY, quality_for_save])

    class Example:
        @staticmethod
        def read_and_show_image(file_path):
            img = cv2.imread(cv2.samples.findFile(file_path))
            cv2.imshow("Display window", img)
            cv2.waitKey(0)

        @staticmethod
        def crop_image(file_path):
            img = cv2.imread(cv2.samples.findFile(file_path))
            height, width, channels = img.shape  # (1920, 1080, 3)
            cv2.imshow("Display window", img)
            cv2.imshow(
                "Display window cropped", img[0 : height // 2, 0 : width // 2]
            )  # y1:y2, x1:x2
            cv2.imshow(
                "Display window cropped2", img[height // 2 : height, width // 2 : width]
            )  # y1:y2, x1:x2
            cv2.waitKey(0)

        @staticmethod
        def change_to_gray_image(file_path):
            img = cv2.imread(
                cv2.samples.findFile(file_path), cv2.IMREAD_GRAYSCALE
            )  # в оперативной памяти
            # img2 = cv2.imread(path, cv2.IMREAD_COLOR)
            # image_gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)  # BGR(RGB) -> GRAY
            cv2.imshow("Display window", img)
            cv2.waitKey(0)

        @staticmethod
        def change_to_bw_image(file_path):
            img = cv2.imread(
                cv2.samples.findFile(file_path), cv2.IMREAD_GRAYSCALE
            )  # в оперативной памяти
            contrast = 90
            image = cv2.threshold(img, contrast, 255, cv2.THRESH_BINARY)[1]
            cv2.imshow("Display window", image)
            cv2.waitKey(0)

        @staticmethod
        def change_quality_image(file_path, quality):
            img = cv2.imread(cv2.samples.findFile(file_path), cv2.IMREAD_COLOR)
            cv2.imwrite(
                f"src/src_avatar_{quality}.jpg",
                img,
                [cv2.IMWRITE_JPEG_QUALITY, quality],
            )

        @staticmethod
        def resize_image(file_path, multiply):
            img = cv2.imread(cv2.samples.findFile(file_path), cv2.IMREAD_COLOR)
            height, width, channels = img.shape  # (1920, 1080, 3)
            multiply: float = multiply / 100  # 1.0 = 100%
            img2 = cv2.resize(img, (int(width * multiply), int(height * multiply)))
            cv2.imshow("Display img", img)
            cv2.imshow("Display img2", img2)
            cv2.waitKey(0)

        @staticmethod
        def detect_faces_and_save_images(directory):
            path = r"data\haarcascade_frontalface_default.xml"
            face_cascade = cv2.CascadeClassifier(path)
            file_extensions = (".jpg", ".jpeg", ".png")

            for filename in os.listdir(directory):
                if filename.lower().endswith(file_extensions):
                    file_path = os.path.join(directory, filename)
                    img = OpenCv.read_image(file_path)
                    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                    faces = face_cascade.detectMultiScale(
                        gray, scaleFactor=1.3, minNeighbors=5
                    )

                    if len(faces) > 0:
                        for i, (x, y, w, h) in enumerate(faces):
                            cropped_img = img[y : y + h, x : x + w]
                            if len(faces) == 1:
                                new_file_path = os.path.join(
                                    "src/output", f"{filename}"
                                )
                            else:
                                new_file_path = os.path.join(
                                    "src/output", f"{i+1}_{filename}"
                                )
                            OpenCv.update_image(
                                cropped_img, new_file_path, "", 90, False, 100
                            )

        @staticmethod
        def detect_faces_video(video_path: str):
            speed: float = 1.0
            cap: cv2.VideoCapture = cv2.VideoCapture(video_path)
            face_cascade = cv2.CascadeClassifier('data\haarcascade_frontalface_default.xml')

            while cap.isOpened():
                ret, frame = cap.read()
                if not ret:
                    break
                
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=4)

                for (x, y, w, h) in faces:
                    cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

                cv2.imshow('Video', frame)
                if cv2.waitKey(int(1000 / (speed * 24))) & 0xFF == ord('q'):
                    break
                
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    ocv = OpenCv()

    ocv.Example.detect_faces_and_save_images(r"src\input")

    ocv.Example.detect_faces_video(r"src\input\face-demographics-walking.mp4")
