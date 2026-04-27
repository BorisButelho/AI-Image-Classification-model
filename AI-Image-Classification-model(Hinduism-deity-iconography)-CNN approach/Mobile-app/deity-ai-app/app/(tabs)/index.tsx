import React, { useRef, useState } from 'react';
import {
  View,
  Text,
  StyleSheet,
  Image,
  ScrollView,
  ActivityIndicator,
  TouchableOpacity
} from 'react-native';
import { CameraView, useCameraPermissions } from 'expo-camera';

export default function HomeScreen() {
  const cameraRef = useRef<any>(null);
  const [permission, requestPermission] = useCameraPermissions();
  const [photo, setPhoto] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);

  const takePicture = async () => {
    if (cameraRef.current) {
      const photoData = await cameraRef.current.takePictureAsync();
      setPhoto(photoData.uri);
      sendToServer(photoData.uri);
    }
  };

  const sendToServer = async (uri: string) => {
    setLoading(true);
    setResult(null);

    const formData = new FormData();
    formData.append('image', {
      uri,
      name: 'photo.jpg',
      type: 'image/jpeg',
    } as any);

    try {
      const response = await fetch('Change YOUR_LOCAL_IP to your PC IPv4 address before running', {
        method: 'POST',
        body: formData,
      });

      const data = await response.json();
      setResult(data);
    } catch (error) {
      console.log(error);
    }

    setLoading(false);
  };

  if (!permission) return <View style={{ flex: 1, backgroundColor: '#000' }} />;

  if (!permission.granted) {
    return (
      <View style={styles.container}>
        <Text style={styles.whiteText}>Camera permission required</Text>
        <TouchableOpacity style={styles.yellowButton} onPress={requestPermission}>
          <Text style={styles.blackText}>Grant Permission</Text>
        </TouchableOpacity>
      </View>
    );
  }

  return (
    <ScrollView contentContainerStyle={styles.container}>
      {!photo ? (
        <CameraView style={styles.camera} ref={cameraRef} />
      ) : (
        <Image source={{ uri: photo }} style={styles.preview} />
      )}

      {/* Capture Button */}
      {!photo && (
        <TouchableOpacity style={styles.captureOuter} onPress={takePicture}>
          <View style={styles.captureInner} />
        </TouchableOpacity>
      )}

      {loading && (
        <View style={{ marginTop: 30 }}>
          <ActivityIndicator size="large" color="#facc15" />
          <Text style={[styles.whiteText, { marginTop: 10 }]}>
            Analyzing Sacred Iconography...
          </Text>
        </View>
      )}

      {result && (
        <View style={styles.resultContainer}>
          <Text style={styles.deityTitle}>
            {result.primary_deity?.toUpperCase()}
          </Text>

          <Text style={styles.confidenceText}>
            Confidence: {result.confidence}
          </Text>

          <Text style={styles.explanationText}>
            {result.explanation}
          </Text>

          <TouchableOpacity
            style={styles.yellowOutlineButton}
            onPress={() => {
              setPhoto(null);
              setResult(null);
            }}
          >
            <Text style={styles.whiteText}>Retake</Text>
          </TouchableOpacity>
        </View>
      )}
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: '#000',
    alignItems: 'center',
    padding: 20,
  },

  camera: {
    width: 340,
    height: 480,
    borderRadius: 18,
    overflow: 'hidden',
  },

  preview: {
    width: 340,
    height: 480,
    borderRadius: 18,
  },

  /* Capture Button */
  captureOuter: {
    width: 80,
    height: 80,
    borderRadius: 40,
    borderWidth: 4,
    borderColor: '#ffffff',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 25,
  },

  captureInner: {
    width: 60,
    height: 60,
    borderRadius: 30,
    backgroundColor: '#ffffff',
  },

  /* Result Styling */
  resultContainer: {
    marginTop: 30,
    width: '100%',
  },

  deityTitle: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#facc15', // subtle yellow accent
    letterSpacing: 2,
  },

  confidenceText: {
    marginTop: 8,
    color: '#ffffff',
    opacity: 0.8,
  },

  explanationText: {
    marginTop: 18,
    color: '#ffffff',
    lineHeight: 22,
    fontSize: 15,
  },

  whiteText: {
    color: '#ffffff',
  },

  blackText: {
    color: '#000000',
  },

  yellowButton: {
    marginTop: 20,
    backgroundColor: '#facc15',
    paddingVertical: 10,
    paddingHorizontal: 25,
    borderRadius: 25,
  },

  yellowOutlineButton: {
    marginTop: 25,
    borderColor: '#facc15',
    borderWidth: 1,
    paddingVertical: 10,
    borderRadius: 25,
    alignItems: 'center',
  },
});