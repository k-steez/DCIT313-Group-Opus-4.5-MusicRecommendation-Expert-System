import { View, Text, StyleSheet } from "react-native";
import { router } from "expo-router";
import { useEffect } from "react";
import {LinearGradient} from "expo-linear-gradient"

export default function Onboarding1() {

  useEffect(() => {
    const timer = setTimeout(() => {
      router.replace("/onboarding2");
    }, 3000); // 3 seconds

    return () => clearTimeout(timer);
  }, []);

  return (
     <LinearGradient colors={["#7B2FF7", "#F107A3", "#FF7A18"]}
      start={{ x: 0, y: 0 }}
      end={{ x: 1, y: 1 }}
      style={styles.container}>
        <View style={styles.container}>
        
          <Text style={styles.logo}>🎵</Text>
          <Text style={styles.title}>MoodBeats</Text>
          <Text style={styles.subtitle}>
            Music that understands your mood.
          </Text>
        </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "#ff4e9b"
  },
  logo: {
    fontSize: 80
  },
  title: {
    fontSize: 40,
    fontWeight: "bold",
    color: "white"
  },
  subtitle: {
    fontSize: 16,
    color: "white",
    marginTop: 10
  }
});