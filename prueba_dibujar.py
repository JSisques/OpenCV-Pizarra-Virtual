import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
width  = cap.get(3)  # float `width`
height = cap.get(4)
print(width, " ", height)

num_cuadrantes_x = 10
num_cuadrantes_y = 5

coordenadas_puntos = []
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

    '''
    #Dibujamos los rectangulos verticales
    cv2.rectangle(image, (0, 0), (int(width / 3 * 1), int(height)), (255,0,0), 3)
    cv2.rectangle(image, (0, 0), (int(width / 3 * 2), int(height)), (0,255,0), 3)
    cv2.rectangle(image, (0, 0), (int(width), int(height)), (0,0,255), 3)

    #Dibujamos los rectangulos horizontales
    cv2.rectangle(image, (0, int(height / 3)), (int(width), int(height / 3)), (255,0,0), 3)
    cv2.rectangle(image, (0, int(height / 3 * 2)), (int(width), int(height / 3 * 2)), (0,255,0), 3)
    cv2.rectangle(image, (0, int(height)), (int(width), int(height)), (0,0,255), 3)
    '''

    #Dibujamos la cuadricula en la imagen
    cuadrantes = []
    for i in range(num_cuadrantes_y):
        ymin = int(height / num_cuadrantes_y * i)
        ymax = int(height / num_cuadrantes_y * (i + 1))

        for j in range(num_cuadrantes_x):
            xmin = int(width / num_cuadrantes_x * j)
            xmax = int(width / num_cuadrantes_x * (j + 1))
            print("Coordenadas:")
            print("Xmin: ", xmin, "Xmax: ", xmax)
            print("Ymin: ", ymin, "Ymax: ", ymax)
            cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0,0,0), 3)
            cuadrantes.append((xmin, ymin, xmax, ymax))

    if results.multi_hand_landmarks:
      for hand_landmarks in results.multi_hand_landmarks:
        
        #Cogemos las coordenadas de la punta del dedo gordo
        #x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x * width)
        #y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y * height)
        #print("Punta del pulgar: ", x1, "\t", y1)

        x1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * width)
        y1 = int(hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * height)
        print("Punta del indice: ", x1, "\t", y1)
        coordenadas_puntos.append((x1,y1))

        mp_drawing.draw_landmarks(
            image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        for i in cuadrantes: 
            xmin = i[0]
            ymin = i[1]
            xmax = i[2]
            ymax = i[3]

            if x1 >= xmin and x1 <= xmax and y1 >= ymin and y1 <= ymax:
                cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0,0,255), -1) # -1 para rellenarlo
                cv2.putText(image, "Estas en el cuadrante: " + str(i), (x1,y1), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (255,0,0), 2)

        for i in coordenadas_puntos:
            cv2.circle(image, i, 3, (255,0,0), 3)

    cv2.imshow('MediaPipe Hands', image)
    print(coordenadas_puntos)
    if cv2.waitKey(5) & 0xFF == ord('q'):
      break
cap.release()
cv2.destroyAllWindows()