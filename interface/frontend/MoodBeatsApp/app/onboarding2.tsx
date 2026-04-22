import { View, Text, StyleSheet, ImageBackground, Dimensions, StatusBar,TouchableOpacity} from "react-native";
import { router } from "expo-router";
import img from "../assets/images/bg1.jpg";
import Button from "@/components/Button";
import {Ionicons} from "@expo/vector-icons"

const { width, height } = Dimensions.get("window");



export default function Onboarding2() {

  const nextPage =() => {
    router.push("/onboarding3")
  };

  const onSkip = () => {
        router.push("/home")
    }
  return (
     <ImageBackground 
          source={img} 
          style={styles.background}
          resizeMode="cover"
        >
          <StatusBar backgroundColor={"pink"}/>
      <View style={styles.container}>
        <TouchableOpacity onPress={onSkip}>
          <Text style={styles.skip}>Skip</Text>
        </TouchableOpacity>
        <View style={styles.musicIcon}>
          <Ionicons name="musical-notes-outline" color={"#FFFFFF"} size={60}/>
        </View>

        <Text style={styles.title}>
          Tell us how you feel
        </Text>

        <Text style={styles.text}>
          Choose from 15 different moods to match your emotional state
        </Text>

        <Button title="Next" onPress={nextPage}/>
      </View>
    </ImageBackground>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
  },
  skip: {
    color:"#FFFFFF",
    position:"relative",
    top:-180,
    right:-30,
    left:150,
    bottom:100
  },
  musicIcon: {
    fontSize: 70,
    backgroundColor: "transparent",
    padding:10,
    height:100,
    width:100,
    borderRadius:50,
    alignItems:"center"
  },
  title: {
    fontSize: 28,
    fontWeight: "bold",
    textAlign: "center",
    color:"#FFFFFF"
  },
  text: {
    textAlign: "center",
    marginTop: 10,
    color:"#FFFFFF"
  },
  background: {
    flex: 1,
    width: width,
    height: height,
  },
});