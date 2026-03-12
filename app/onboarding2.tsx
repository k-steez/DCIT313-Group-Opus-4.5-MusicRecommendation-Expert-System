import { View, Text, Button, StyleSheet } from "react-native";
import { router } from "expo-router";

export default function Onboarding2() {
  return (
    <View style={styles.container}>
      <Text style={styles.icon}>🎵</Text>

      <Text style={styles.title}>
        Tell us how you feel
      </Text>

      <Text style={styles.text}>
        Choose from 15 different moods to match your emotional state
      </Text>

      <Button title="Next" onPress={() => router.push("/home")} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    backgroundColor:"#ff4e9b"
  },
  icon: {
    fontSize: 70,
    backgroundColor: "#dee2e6"
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    textAlign: "center"
  },
  text: {
    textAlign: "center",
    marginTop: 10
  }
});