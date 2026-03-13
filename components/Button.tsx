import { View, Text, TouchableOpacity, StyleSheet } from 'react-native'
import React from 'react'

type ButtonProps = {
    title: string,
    onPress: () => void;
}

const Button = ({title,onPress}:ButtonProps) => {
  return (
    <View style={styles.container}>
      <TouchableOpacity style={styles.button} onPress={onPress}>
        <Text>{title}</Text>
      </TouchableOpacity>
    </View>
  )
}

const styles = StyleSheet.create({
    container:{
        backgroundColor: "#FFFFFF",
        padding: 18,
        width:'80%',
        marginHorizontal:30,
        marginVertical:15,
        borderRadius:16,
        bottom:-230
    },
    button:{
        alignItems:"center",
        fontSize:24,
        opacity: 10
    }
})

export default Button