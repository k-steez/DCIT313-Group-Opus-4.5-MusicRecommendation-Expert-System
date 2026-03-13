import { View, Text, StyleSheet, Dimensions } from 'react-native';
import React, { useEffect, useState } from 'react';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather } from '@expo/vector-icons';
import Animated, { 
  useSharedValue, 
  useAnimatedStyle, 
  withTiming, 
  withRepeat,
  withSequence,
  Easing
} from 'react-native-reanimated';

const { width } = Dimensions.get('window');

// Messages to cycle through while loading
const LOADING_MESSAGES = [
  "Filtering by activity requirements...",
  "Optimizing for your current task...",
  "Finding the perfect BPM...",
  "Curating your MoodBeats..."
];

export default function LoadingScreen() {
  const [messageIndex, setMessageIndex] = useState(0);
  
  // Animation values
  const progressWidth = useSharedValue(0);
  const pulseScale = useSharedValue(1);
  const pulseOpacity = useSharedValue(1);

  useEffect(() => {
    // 1. Start the progress bar animation (simulate loading over 4 seconds)
    progressWidth.value = withTiming(100, {
      duration: 4000,
      easing: Easing.inOut(Easing.ease)
    });

    // 2. Start the pulsing animation for the icons
    pulseScale.value = withRepeat(
      withSequence(
        withTiming(1.1, { duration: 1000 }),
        withTiming(1, { duration: 1000 })
      ),
      -1,
      true
    );

    pulseOpacity.value = withRepeat(
      withSequence(
        withTiming(0.6, { duration: 1000 }),
        withTiming(1, { duration: 1000 })
      ),
      -1,
      true
    );

    // 3. Cycle through messages every 1.2 seconds
    const messageInterval = setInterval(() => {
      setMessageIndex((prev) => (prev + 1) % LOADING_MESSAGES.length);
    }, 1200);

    // 4. Navigate to the final playlist screen after 4 seconds
    const timeout = setTimeout(() => {
      router.replace('/playlist');
    }, 4200);

    return () => {
      clearInterval(messageInterval);
      clearTimeout(timeout);
    };
  }, []);

  const animatedProgressStyle = useAnimatedStyle(() => {
    return {
      width: `${progressWidth.value}%`
    };
  });

  const animatedPulseStyle = useAnimatedStyle(() => {
    return {
      transform: [{ scale: pulseScale.value }],
      opacity: pulseOpacity.value
    };
  });

  return (
    <LinearGradient 
      colors={['#7E22CE', '#BE185D', '#DB2777']} 
      style={styles.container}
      locations={[0, 0.7, 1]}
    >
      <View style={styles.content}>
        
        {/* Top Icons */}
        <Animated.View style={[styles.iconRow, animatedPulseStyle]}>
          <View style={styles.iconCircleBackground}>
            <Feather name="music" size={48} color="#ffffff" style={styles.iconShift1} />
          </View>
          <View style={[styles.iconCircleBackground, styles.iconOverlap]}>
            <Feather name="filter" size={48} color="#ffffff" style={styles.iconShift2} />
          </View>
        </Animated.View>

        {/* Center Activity Icon */}
        <Animated.View style={[styles.centerIconContainer, animatedPulseStyle]}>
          <Feather name="activity" size={80} color="#ffffff" />
        </Animated.View>

        {/* Loading Text */}
        <View style={styles.textContainer}>
          <Text style={styles.loadingText}>
            {LOADING_MESSAGES[messageIndex].split('\n').map((line, i) => (
               <Text key={i}>{line}{'\n'}</Text>
            ))}
          </Text>
        </View>

        {/* Progress Stages UI (Static visual representation for design match) */}
        <View style={styles.stagesContainer}>
          <View style={styles.stageCircleActive}>
            <Feather name="music" size={16} color="#A800FF" />
          </View>
          <Feather name="chevron-right" size={16} color="rgba(255,255,255,0.6)" />
          
          <View style={styles.stageCircleActive}>
            <Feather name="filter" size={16} color="#A800FF" />
          </View>
          <Feather name="chevron-right" size={16} color="rgba(255,255,255,0.6)" />
          
          <View style={styles.stageCircleHalf}>
            <Feather name="activity" size={16} color="#A800FF" />
          </View>
          <Feather name="chevron-right" size={16} color="rgba(255,255,255,0.4)" />
          
          <View style={styles.stageCircleInactive}>
            <Feather name="list" size={16} color="rgba(255,255,255,0.4)" />
          </View>
        </View>

        {/* Progress Bar Container */}
        <View style={styles.progressBarContainer}>
          <View style={styles.progressBarBackground}>
             <Animated.View style={[styles.progressFill, animatedProgressStyle]} />
          </View>
        </View>
        
      </View>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  content: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 30,
  },
  iconRow: {
    flexDirection: 'row',
    marginBottom: 80,
    justifyContent: 'center',
  },
  iconCircleBackground: {
    width: 130,
    height: 130,
    borderRadius: 65,
    backgroundColor: 'rgba(255, 255, 255, 0.15)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  iconOverlap: {
    marginLeft: -30, // Create the overlapping Venn diagram effect
  },
  iconShift1: {
    marginRight: 10,
  },
  iconShift2: {
    marginLeft: 10,
  },
  centerIconContainer: {
    marginBottom: 60,
  },
  textContainer: {
    height: 80, // Fixed height to prevent layout jumps when text changes
    justifyContent: 'center',
    marginBottom: 40,
  },
  loadingText: {
    fontSize: 22,
    fontWeight: '700',
    color: 'rgba(255, 255, 255, 0.95)',
    textAlign: 'center',
    lineHeight: 32,
  },
  stagesContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: 30,
    gap: 12, // For react-native >= 0.71, otherwise use margin
  },
  stageCircleActive: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: '#ffffff',
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
  },
  stageCircleHalf: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(255, 255, 255, 0.5)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  stageCircleInactive: {
    width: 36,
    height: 36,
    borderRadius: 18,
    backgroundColor: 'rgba(255, 255, 255, 0.1)',
    justifyContent: 'center',
    alignItems: 'center',
  },
  progressBarContainer: {
    width: '100%',
    paddingHorizontal: 20,
  },
  progressBarBackground: {
    height: 8,
    backgroundColor: 'rgba(255, 255, 255, 0.2)',
    borderRadius: 4,
    width: '100%',
    overflow: 'hidden',
  },
  progressFill: {
    height: '100%',
    backgroundColor: '#ffffff',
    borderRadius: 4,
  }
});
