from decimal import Decimal

from store.models import Product


class Cart():
    def __init__(self, request):
        
        self.session = request.session
        cart = self.session.get('session_key')
        
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
                        
        self.cart = cart
        
        
    def add(self, product, product_quantity):
        product_id = str(product.id)
        
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_quantity
            
        else:
            self.cart[product_id] = {'price': str(product.price), 'quantity': product_quantity}
            
            self.session.modified = True
        
        
    def delete(self, product):
        product_id = str(product)
        
        if product_id in self.cart:
            del self.cart[product_id]
            
        self.session.modified = True
        
        
    def update(self, product, quantity):
        product_id = str(product)
        product_quantity = quantity
        
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_quantity
            
        self.session.modified = True
        
        
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())
    
    
    def __iter__(self):
        all_product_ids = self.cart.keys()
        
        products = Product.objects.filter(id__in=all_product_ids)
        
        import copy
        cart = copy.deepcopy(self.cart)
        
        for product in products:
            cart[str(product.id)]['product'] = product
            
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['quantity']
            
            yield item
            
            
    def get_total(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())