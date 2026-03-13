import { View, Text, StyleSheet, TouchableOpacity, ScrollView } from 'react-native';
import React from 'react';
import { router } from 'expo-router';
import { LinearGradient } from 'expo-linear-gradient';
import { Feather } from '@expo/vector-icons';
import { SafeAreaView } from 'react-native-safe-area-context';

export default function AboutScreen() {
  return (
    <LinearGradient 
      colors={['#ffffff', '#fcfaff', '#faf5ff']} 
      style={styles.container}
    >
      <SafeAreaView style={styles.safeArea}>
        
        {/* Header */}
        <View style={styles.header}>
          <TouchableOpacity 
            style={styles.backButton}
            onPress={() => router.back()}
          >
            <Feather name="chevron-left" size={24} color="#374151" />
          </TouchableOpacity>
          <Text style={styles.headerTitle}>About MoodBeats</Text>
          {/* Invisible flex balancer */}
          <View style={{ width: 44 }} />
        </View>

        <ScrollView 
          showsVerticalScrollIndicator={false}
          contentContainerStyle={styles.scrollContent}
        >
          {/* Hero Section */}
          <View style={styles.heroSection}>
            <LinearGradient
              colors={['#CC00FF', '#FF007F']}
              start={{ x: 0, y: 0 }}
              end={{ x: 1, y: 1 }}
              style={styles.heroIconContainer}
            >
              <Feather name="music" size={48} color="#ffffff" />
            </LinearGradient>
            
            <Text style={styles.heroTitle}>MoodBeats</Text>
            <Text style={styles.heroSubtitle}>Music that understands your mood</Text>
          </View>

          {/* Description Card */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>What is MoodBeats?</Text>
            <Text style={styles.cardBody}>
              MoodBeats is an intelligent music recommendation system that uses rule-based expert reasoning grounded in music psychology.
              {'\n\n'}
              We analyze your emotional state and current activity to curate the perfect playlist that matches both your mood and needs.
            </Text>
          </View>

          {/* How It Works Card */}
          <View style={styles.card}>
            <Text style={styles.cardTitle}>How it works</Text>
            
            <View style={styles.stepContainer}>
              <LinearGradient
                colors={['#CC00FF', '#FF007F']}
                style={styles.stepIconBox}
              >
                <Feather name="music" size={20} color="#ffffff" />
              </LinearGradient>
              <View style={styles.stepTextContent}>
                <Text style={styles.stepTitle}>1. Mood Selection</Text>
                <Text style={styles.stepBody}>
                  Choose from 15 scientifically categorized moods based on emotional energy and valence.
                </Text>
              </View>
            </View>

            <View style={styles.stepContainer}>
              <LinearGradient
                colors={['#CC00FF', '#FF007F']}
                style={styles.stepIconBox}
              >
                <Feather name="activity" size={20} color="#ffffff" />
              </LinearGradient>
              <View style={styles.stepTextContent}>
                <Text style={styles.stepTitle}>2. Activity Refinement</Text>
                <Text style={styles.stepBody}>
                  Filter generated recommendations appropriately structured around cognitive workloads and temporal limits.
                </Text>
              </View>
            </View>

          </View>

        </ScrollView>
      </SafeAreaView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  safeArea: {
    flex: 1,
  },
  header: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingHorizontal: 20,
    paddingTop: 10,
    paddingBottom: 20,
  },
  backButton: {
    width: 44,
    height: 44,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 22,
    fontWeight: '800',
    color: '#1f2937',
  },
  scrollContent: {
    paddingHorizontal: 20,
    paddingBottom: 40,
  },
  heroSection: {
    alignItems: 'center',
    marginTop: 10,
    marginBottom: 40,
  },
  heroIconContainer: {
    width: 100,
    height: 100,
    borderRadius: 50,
    justifyContent: 'center',
    alignItems: 'center',
    shadowColor: '#CC00FF',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 8,
    marginBottom: 20,
  },
  heroTitle: {
    fontSize: 32,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 8,
  },
  heroSubtitle: {
    fontSize: 16,
    color: '#6b7280',
    fontWeight: '500',
  },
  card: {
    backgroundColor: '#ffffff',
    borderRadius: 24,
    padding: 24,
    marginBottom: 24,
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 6 },
    shadowOpacity: 0.04,
    shadowRadius: 12,
    elevation: 3,
    borderWidth: 1,
    borderColor: '#f9fafb',
  },
  cardTitle: {
    fontSize: 20,
    fontWeight: '800',
    color: '#1f2937',
    marginBottom: 16,
  },
  cardBody: {
    fontSize: 16,
    color: '#4b5563',
    lineHeight: 26,
  },
  stepContainer: {
    flexDirection: 'row',
    marginBottom: 24,
  },
  stepIconBox: {
    width: 44,
    height: 44,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 16,
  },
  stepTextContent: {
    flex: 1,
  },
  stepTitle: {
    fontSize: 16,
    fontWeight: '700',
    color: '#1f2937',
    marginBottom: 6,
  },
  stepBody: {
    fontSize: 14,
    color: '#6b7280',
    lineHeight: 22,
  }
});
