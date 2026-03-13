import { View, Text, StyleSheet, ImageBackground, Dimensions } from "react-native";
import { router } from "expo-router";
import { useEffect } from "react";
import img from "../assets/images/bg3.jpg";

const { width, height } = Dimensions.get("window");

export default function Onboarding1() {
  useEffect(() => {
    const timer = setTimeout(() => {
      router.replace("/onboarding2");
    }, 4000); // 4 seconds

    return () => clearTimeout(timer);
  }, []);

  return (
    <ImageBackground 
      source={img} 
      style={styles.background}
      resizeMode="cover"
    >
      <View style={styles.overlay}>
        <View style={styles.container}>
          <Text style={styles.logo}>🎵</Text>
          <Text style={styles.title}>MoodBeats</Text>
          <Text style={styles.subtitle}>
            Music that understands your mood.
          </Text>
        </View>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: width,
    height: height,
  },
  overlay: {
    flex: 1,
    backgroundColor: 'rgba(0, 0, 0, 0.3)', // Semi-transparent overlay for better text readability
  },
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: 20,
  },
  logo: {
    fontSize: 80,
    marginBottom: 10,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 5,
  },
  title: {
    fontSize: 48,
    fontWeight: "bold",
    color: "white",
    textAlign: "center",
    letterSpacing: 1,
    marginBottom: 10,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 2, height: 2 },
    textShadowRadius: 5,
  },
  subtitle: {
    fontSize: 18,
    color: "white",
    textAlign: "center",
    opacity: 0.95,
    fontWeight: "500",
    letterSpacing: 0.5,
    textShadowColor: 'rgba(0, 0, 0, 0.3)',
    textShadowOffset: { width: 1, height: 1 },
    textShadowRadius: 3,
  }
});