from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import ProductSerializer
from rest_framework.response import Response
from rest_framework import status
from .models import Product

# Create your views here.

# Add a product
class AddProductView(GenericAPIView):
    serializer_class = ProductSerializer

    def post(self, request):
        products = request.data  # Directly get the list of products

        if isinstance(products, list):  # Check if the data is a list
            for product_data in products:
                # Create serializer for each product
                product_serializer = ProductSerializer(data=product_data)
                
                if product_serializer.is_valid():
                    product_serializer.save()
                else:
                    return Response(
                        {
                            "Message": "Validation error",
                            "Errors": product_serializer.errors,
                            "Product": product_data
                        },
                        status=status.HTTP_400_BAD_REQUEST,
                    )

            return Response(
                {"Message": "All products added successfully"}, status=status.HTTP_201_CREATED
            )
        else:
            return Response(
                {"Message": "Expected a list of products"},
                status=status.HTTP_400_BAD_REQUEST,
            )

class GetProductsView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        a = Product.objects.all()
        if a.exists():
            b = ProductSerializer(a, many=True)
            return Response(
                {"data": b.data, "Message": "Fetch succesful"},
                status=status.HTTP_200_OK,
            )
        else:
            return Response({"Message": "No data"}, status=status.HTTP_400_BAD_REQUEST)


class AyishaView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()
        
        if products.exists():
            structured_data = []

            # Loop through the products and nest the structure deeply
            for product in products:
                structured_data.append({
                    "meta": {
                        "productID": product.id,
                        "details": {
                            "info": {
                                "titleDesc": {
                                    "name": product.title,
                                    "longDesc": product.description
                                },
                                "pricing": {
                                    "cost": product.price
                                },
                                "categoryType": {
                                    "cat": product.category
                                },
                                "images": {
                                    "mainImg": {
                                        "url": product.image if product.image else None
                                    }
                                }
                            }
                        }
                    }
                })

            # Create more complex layers with subgroups
            response_data = {
                "payload": {
                    "dataGroup": [
                        {
                            "itemsList": structured_data[:2],  # First two products in this group
                        },
                        {
                            "subItemsGroup": [
                                {
                                    "element": {
                                        "meta": structured_data[2]["meta"] if len(structured_data) > 2 else None,
                                    }
                                },
                                {
                                    "element": {
                                        "meta": structured_data[3]["meta"] if len(structured_data) > 3 else None,
                                    }
                                }
                            ]
                        },
                        {
                            "subPayload": {
                                "nestedList": [
                                    {
                                        "component": {
                                            "infoBlock": {
                                                "productData": {
                                                    "uniqueID": structured_data[4]["meta"]["productID"] if len(structured_data) > 4 else None,
                                                    "descriptionBlock": structured_data[4]["meta"]["details"]["info"] if len(structured_data) > 4 else None,
                                                    "costing": structured_data[4]["meta"]["details"]["info"]["pricing"] if len(structured_data) > 4 else None,
                                                    "categoryGroup": {
                                                        "name": structured_data[4]["meta"]["details"]["info"]["categoryType"]["cat"] if len(structured_data) > 4 else None
                                                    },
                                                    "visualContent": {
                                                        "primaryImage": structured_data[4]["meta"]["details"]["info"]["images"]["mainImg"]["url"] if len(structured_data) > 4 else None
                                                    }
                                                }
                                            }
                                        }
                                    },
                                    {
                                        "component": {
                                            "infoBlock": {
                                                "productData": {
                                                    "uniqueID": structured_data[5]["meta"]["productID"] if len(structured_data) > 5 else None,
                                                    "descriptionBlock": structured_data[5]["meta"]["details"]["info"] if len(structured_data) > 5 else None,
                                                    "costing": structured_data[5]["meta"]["details"]["info"]["pricing"] if len(structured_data) > 5 else None,
                                                    "categoryGroup": {
                                                        "name": structured_data[5]["meta"]["details"]["info"]["categoryType"]["cat"] if len(structured_data) > 5 else None
                                                    },
                                                    "visualContent": {
                                                        "primaryImage": structured_data[5]["meta"]["details"]["info"]["images"]["mainImg"]["url"] if len(structured_data) > 5 else None
                                                    }
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        },
                        {
                            "moreData": {
                                "productsBlock": [
                                    {
                                        "data": {
                                            "metaInfo": {
                                                "prodID": structured_data[6]["meta"]["productID"] if len(structured_data) > 6 else None,
                                                "descriptionInfo": structured_data[6]["meta"]["details"]["info"] if len(structured_data) > 6 else None,
                                                "pricingDetails": structured_data[6]["meta"]["details"]["info"]["pricing"] if len(structured_data) > 6 else None,
                                                "categoryLabel": structured_data[6]["meta"]["details"]["info"]["categoryType"]["cat"] if len(structured_data) > 6 else None,
                                                "imageBlock": {
                                                    "imagePath": structured_data[6]["meta"]["details"]["info"]["images"]["mainImg"]["url"] if len(structured_data) > 6 else None
                                                }
                                            }
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                },
                "statusMessage": "Fetched successfully"
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "No products found"}, status=status.HTTP_400_BAD_REQUEST)
        
class SagarView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()

        if products.exists():
            structured_data = []

            for product in products:
                structured_data.append({
                    "metadata": {
                        "productDetails": {
                            "ID": product.id,
                            "info": {
                                "title": product.title,
                                "description": product.description
                            },
                            "pricing": {
                                "amount": product.price,
                                "currency": "USD",
                                "discounted": product.price and float(product.price) * 0.9  # Assuming a 10% discount
                            },
                            "category": product.category
                        },
                        "media": {
                            "image": {
                                "url": product.image if product.image else None,
                                "altText": f"Image of {product.title}"
                            }
                        },
                        "availability": {
                            "inStock": True if product.price else False,
                            "shipping": "Free"  # Assuming free shipping for simplicity
                        }
                    }
                })

            response_data = {
                "responseData": {
                    "categoryGroups": {
                        "electronics": {
                            "details": {
                                "count": len([item for item in structured_data if item["metadata"]["productDetails"]["category"] == "Electronics"]),
                                "totalValue": sum(float(item["metadata"]["productDetails"]["pricing"]["amount"]) for item in structured_data if item["metadata"]["productDetails"]["category"] == "Electronics")
                            },
                            "items": [item for item in structured_data if item["metadata"]["productDetails"]["category"] == "Electronics"]
                        },
                        "wearables": {
                            "details": {
                                "count": len([item for item in structured_data if item["metadata"]["productDetails"]["category"] == "Wearables"]),
                                "totalValue": sum(float(item["metadata"]["productDetails"]["pricing"]["amount"]) for item in structured_data if item["metadata"]["productDetails"]["category"] == "Wearables")
                            },
                            "items": [item for item in structured_data if item["metadata"]["productDetails"]["category"] == "Wearables"]
                        },
                        "footwear": {
                            "details": {
                                "count": len([item for item in structured_data if item["metadata"]["productDetails"]["category"] == "Footwear"]),
                                "totalValue": sum(float(item["metadata"]["productDetails"]["pricing"]["amount"]) for item in structured_data if item["metadata"]["productDetails"]["category"] == "Footwear")
                            },
                            "items": [item for item in structured_data if item["metadata"]["productDetails"]["category"] == "Footwear"]
                        }
                    },
                    "summary": {
                        "totalProducts": len(structured_data),
                        "totalValueAllCategories": sum(float(item["metadata"]["productDetails"]["pricing"]["amount"]) for item in structured_data)
                    }
                },
                "statusMessage": "Fetch successful",
                "metadata": {
                    "responseTime": "0.23 seconds",  # Example response time
                    "version": "1.0"
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "No products found"}, status=status.HTTP_400_BAD_REQUEST)

        
class RameesView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()

        if products.exists():
            structured_data = []

            for product in products:
                # Convert price to float and handle potential conversion errors
                try:
                    price_amount = float(product.price)
                except (ValueError, TypeError):
                    price_amount = 0.0

                # Calculate discount amount
                discount_amount = price_amount * 0.10

                structured_data.append({
                    "productDetail": {
                                                    "name": "Ramees",

                        "id": product.id,
                        "attributes": {
                            "title": product.title,
                            "description": product.description,
                            "price": {
                                "amount": price_amount,
                                "currency": "USD",
                                "discount": {
                                    "percentage": 10,  # Example discount percentage
                                    "amount": discount_amount
                                }
                            },
                            "category": product.category,
                            "tags": ["new", "featured", "limited"],  # Example tags
                            "condition": "New"  # Example condition
                        },
                        "media": {
                            "images": {
                                "mainImage": product.image if product.image else None,
                                "thumbnail": product.image if product.image else None,  # Example thumbnail
                                "gallery": [
                                    "http://example.com/image1.jpg",
                                    "http://example.com/image2.jpg"  # Example additional images
                                ]
                            },
                            "video": {
                                "url": "http://example.com/video.mp4",  # Example video URL
                                "duration": "2 minutes"  # Example video duration
                            }
                        },
                        "availability": {
                            "inStock": True if price_amount > 0 else False,
                            "availabilityDetails": {
                                "shipping": {
                                    "status": "Free",
                                    "estimatedDelivery": "3-5 business days",
                                    "trackingAvailable": True
                                },
                                "warranty": "1 year"  # Example warranty information
                            }
                        }
                    }
                })

            # Define categories and their products
            category_products = {
                "Electronics": [item for item in structured_data if item["productDetail"]["attributes"]["category"] == "Electronics"],
                "Wearables": [item for item in structured_data if item["productDetail"]["attributes"]["category"] == "Wearables"],
                "Footwear": [item for item in structured_data if item["productDetail"]["attributes"]["category"] == "Footwear"]
            }

            # Calculate statistics for each category
            category_summary = {}
            for category, items in category_products.items():
                category_summary[category] = {
                    "totalProducts": len(items),
                    "averagePrice": sum(float(item["productDetail"]["attributes"]["price"]["amount"]) for item in items) / len(items) if items else 0,
                    "priceRange": {
                        "min": min(float(item["productDetail"]["attributes"]["price"]["amount"]) for item in items) if items else 0,
                        "max": max(float(item["productDetail"]["attributes"]["price"]["amount"]) for item in items) if items else 0
                    },
                    "availabilityStats": {
                        "inStock": sum(1 for item in items if item["productDetail"]["availability"]["inStock"]),
                        "outOfStock": len(items) - sum(1 for item in items if item["productDetail"]["availability"]["inStock"])
                    },
                    "tags": list(set(tag for item in items for tag in item["productDetail"]["attributes"]["tags"]))  # Aggregate tags
                }

            response_data = {
                "result": {
                    "overview": {
                        "totalProducts": len(structured_data),
                        "categories": {
                            "all": {
                                "count": len(structured_data),
                                "items": structured_data
                            },
                            "categoryDetails": category_summary
                        }
                    },
                    "detailedView": {
                        "categoryGroups": [
                            {
                                "groupName": category,
                                "products": items,
                                "groupSummary": summary
                            } for category, (items, summary) in zip(category_products.keys(), zip(category_products.values(), category_summary.values()))
                        ]
                    }
                },
                "status": "success",
                "metadata": {
                    "responseTime": "0.45 seconds",  # Example response time
                    "version": "1.1",
                    "requestID": "REQ-987654",  # Example request ID
                    "serverDetails": {
                        "serverName": "Server-1",
                        "load": "10%"
                    }
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "No products found"}, status=status.HTTP_400_BAD_REQUEST)





        
class ShibinView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()

        if products.exists():
            structured_data = []

            for product in products:
                structured_data.append({
                    "productInformation": {
                        "identifier": {
                            "name": "Shibin",
                            "productID": product.id,
                            "externalID": f"EXT-{product.id}"  # Example external ID
                        },
                        "details": {
                            "name": product.title,
                            "description": product.description,
                            "price": {
                                "amount": product.price,
                                "currency": "USD"
                            },
                            "category": {
                                "mainCategory": product.category,
                                "subCategory": "N/A"  # Example placeholder for subcategory
                            },
                            "availability": {
                                "inStock": True if product.price else False,
                                "shipping": {
                                    "status": "Free",
                                    "expectedDelivery": "3-5 business days"
                                }
                            }
                        },
                        "media": {
                            "images": {
                                "mainImage": product.image if product.image else None,
                                "thumbnail": product.image if product.image else None,
                                "gallery": [product.image] if product.image else []
                            }
                        }
                    }
                })

            electronics = [item for item in structured_data if item["productInformation"]["details"]["category"]["mainCategory"] == "Electronics"]
            wearables = [item for item in structured_data if item["productInformation"]["details"]["category"]["mainCategory"] == "Wearables"]
            footwear = [item for item in structured_data if item["productInformation"]["details"]["category"]["mainCategory"] == "Footwear"]

            category_summary = {
                "Electronics": {
                    "count": len(electronics),
                    "averagePrice": sum(float(item["productInformation"]["details"]["price"]["amount"]) for item in electronics) / len(electronics) if electronics else 0,
                    "availabilityStats": {
                        "inStock": sum(1 for item in electronics if item["productInformation"]["details"]["availability"]["inStock"]),
                        "outOfStock": len(electronics) - sum(1 for item in electronics if item["productInformation"]["details"]["availability"]["inStock"])
                    }
                },
                "Wearables": {
                    "count": len(wearables),
                    "averagePrice": sum(float(item["productInformation"]["details"]["price"]["amount"]) for item in wearables) / len(wearables) if wearables else 0,
                    "availabilityStats": {
                        "inStock": sum(1 for item in wearables if item["productInformation"]["details"]["availability"]["inStock"]),
                        "outOfStock": len(wearables) - sum(1 for item in wearables if item["productInformation"]["details"]["availability"]["inStock"])
                    }
                },
                "Footwear": {
                    "count": len(footwear),
                    "averagePrice": sum(float(item["productInformation"]["details"]["price"]["amount"]) for item in footwear) / len(footwear) if footwear else 0,
                    "availabilityStats": {
                        "inStock": sum(1 for item in footwear if item["productInformation"]["details"]["availability"]["inStock"]),
                        "outOfStock": len(footwear) - sum(1 for item in footwear if item["productInformation"]["details"]["availability"]["inStock"])
                    }
                }
            }

            response_data = {
                "dataLayer": {
                    "productGroups": [
                        {
                            "groupName": "Category Breakdown",
                            "categories": {
                                "Electronics": {
                                    "items": electronics,
                                    "summary": category_summary["Electronics"],
                                    "subGroups": {
                                        "HighEnd": [item for item in electronics if float(item["productInformation"]["details"]["price"]["amount"]) > 1000],
                                        "MidRange": [item for item in electronics if 500 <= float(item["productInformation"]["details"]["price"]["amount"]) <= 1000],
                                        "Budget": [item for item in electronics if float(item["productInformation"]["details"]["price"]["amount"]) < 500]
                                    }
                                },
                                "Wearables": {
                                    "items": wearables,
                                    "summary": category_summary["Wearables"]
                                },
                                "Footwear": {
                                    "items": footwear,
                                    "summary": category_summary["Footwear"]
                                }
                            }
                        },
                        {
                            "groupName": "Product Overview",
                            "totalProducts": len(structured_data),
                            "totalCategories": len(category_summary),
                            "products": structured_data,
                            "detailedSummary": {
                                "totalValue": sum(float(item["productInformation"]["details"]["price"]["amount"]) for item in structured_data),
                                "averagePrice": sum(float(item["productInformation"]["details"]["price"]["amount"]) for item in structured_data) / len(structured_data) if structured_data else 0
                            }
                        }
                    ],
                    "metadata": {
                        "responseTime": "0.45 seconds",  # Example response time
                        "version": "2.0",
                        "requestID": "REQ-123456"  # Example request ID
                    }
                },
                "status": "Data retrieved successfully"
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "No products found"}, status=status.HTTP_400_BAD_REQUEST)



class SreeyukthaView(GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request):
        products = Product.objects.all()

        if products.exists():
            structured_data = []

            for product in products:
                structured_data.append({
                    "productAttributes": {
                        "identifier": {
                            "id": product.id,
                            "name": "Sreeyuktha"
                        },
                        "details": {
                            "title": product.title,
                            "description": product.description,
                            "price": {
                                "amount": product.price,
                                "currency": "USD"
                            },
                            "category": product.category,
                            "tags": ["new", "limited"]  # Example tags
                        },
                        "mediaFiles": {
                            "imageLinks": {
                                "main": product.image if product.image else None,
                                "thumbnail": product.image if product.image else None  # Example thumbnail
                            },
                            "videoLinks": [
                                "http://example.com/video.mp4"  # Placeholder video URL
                            ]
                        },
                        "availability": {
                            "inStock": True if product.price else False,
                            "availabilityDetails": {
                                "shipping": "Free",
                                "estimatedDelivery": "5-7 business days",
                                "stockStatus": "Available" if product.price else "Out of Stock"
                            }
                        }
                    }
                })

            # Define categories and their products
            category_products = {
                "Electronics": [item for item in structured_data if item["productAttributes"]["details"]["category"] == "Electronics"],
                "Wearables": [item for item in structured_data if item["productAttributes"]["details"]["category"] == "Wearables"],
                "Footwear": [item for item in structured_data if item["productAttributes"]["details"]["category"] == "Footwear"],
                "Accessories": [item for item in structured_data if item["productAttributes"]["details"]["category"] == "Accessories"]
            }

            # Calculate detailed statistics and aggregated data
            category_summary = {}
            for category, items in category_products.items():
                category_summary[category] = {
                    "totalProducts": len(items),
                    "averagePrice": sum(float(item["productAttributes"]["details"]["price"]["amount"]) for item in items) / len(items) if items else 0,
                    "priceRange": {
                        "min": min(float(item["productAttributes"]["details"]["price"]["amount"]) for item in items) if items else 0,
                        "max": max(float(item["productAttributes"]["details"]["price"]["amount"]) for item in items) if items else 0
                    },
                    "tags": list(set(tag for item in items for tag in item["productAttributes"]["details"]["tags"])),  # Aggregate tags
                    "availabilityStats": {
                        "inStock": sum(1 for item in items if item["productAttributes"]["availability"]["inStock"]),
                        "outOfStock": len(items) - sum(1 for item in items if item["productAttributes"]["availability"]["inStock"])
                    },
                    "priceDistribution": {
                        "under100": len([item for item in items if float(item["productAttributes"]["details"]["price"]["amount"]) < 100]),
                        "100to500": len([item for item in items if 100 <= float(item["productAttributes"]["details"]["price"]["amount"]) <= 500]),
                        "above500": len([item for item in items if float(item["productAttributes"]["details"]["price"]["amount"]) > 500])
                    }
                }

            # Compute high-level statistics
            overall_stats = {
                "totalProductCount": len(structured_data),
                "averagePrice": sum(float(item["productAttributes"]["details"]["price"]["amount"]) for item in structured_data) / len(structured_data) if structured_data else 0,
                "highestPricedProduct": max(structured_data, key=lambda x: float(x["productAttributes"]["details"]["price"]["amount"]), default=None),
                "lowestPricedProduct": min(structured_data, key=lambda x: float(x["productAttributes"]["details"]["price"]["amount"]), default=None),
                "totalCategories": len(category_summary),
                "tagsOverview": list(set(tag for item in structured_data for tag in item["productAttributes"]["details"]["tags"]))
            }

            response_data = {
                "responseDetails": {
                    "dataOverview": {
                        "productCount": len(structured_data),
                        "products": structured_data,
                        "totalCategories": len(category_summary)
                    },
                    "categorySegmentation": {
                        "categories": category_summary,
                        "subcategoryGroups": [
                            {
                                "groupName": "Top Categories",
                                "categories": [
                                    {
                                        "categoryName": category,
                                        "details": summary
                                    } for category, summary in category_summary.items()
                                ]
                            }
                        ]
                    },
                    "highlights": {
                        "highestPricedProduct": overall_stats["highestPricedProduct"],
                        "lowestPricedProduct": overall_stats["lowestPricedProduct"]
                    },
                    "priceDistribution": {
                        "distribution": {category: summary["priceDistribution"] for category, summary in category_summary.items()}
                    }
                },
                "status": "Data successfully fetched",
                "metadata": {
                    "responseTime": "0.50 seconds",  # Example response time
                    "version": "2.0",
                    "requestID": "REQ-789012",  # Example request ID
                    "serverDetails": {
                        "serverName": "Server-5",
                        "load": "18%"
                    }
                }
            }

            return Response(response_data, status=status.HTTP_200_OK)
        else:
            return Response({"Message": "No products found"}, status=status.HTTP_400_BAD_REQUEST)





