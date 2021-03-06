import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
width  = cap.get(3)  # float `width`
height = cap.get(4)

print(width, " ", height)
coordenadas_dibujo = []

def main():
    with mp_hands.Hands(
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5) as hands:
        while cap.isOpened():
            success, image = cap.read()
            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                continue

            # Flip the image horizontally for a later selfie-view display, and convert
            # the BGR image to RGB.
            image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
            # To improve performance, optionally mark the image as not writeable to
            # pass by reference.
            image.flags.writeable = False
            results = hands.process(image)

            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            if results.multi_hand_landmarks:
                for hand_landmarks in results.multi_hand_landmarks:

                    x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
                    y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
                    print("Punta del indice: ", x1, "\t", y1)
                    coordenadas_dibujo.append((x1, y1))

                    mp_drawing.draw_landmarks(
                        image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            draw(image)
            cv2.imshow('MediaPipe Hands', image)
            
            if cv2.waitKey(5) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()

def draw(image):
    for i in coordenadas_dibujo:
        cv2.circle(image, i, 2, (255,255,255), 3)

main()